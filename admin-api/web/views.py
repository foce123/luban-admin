import json
import uuid

from addict import Dict
from django.http.response import JsonResponse
from django_redis import get_redis_connection
from rest_framework.views import APIView

from config import config
from utils.myDataUtils import TreeBuilder
from utils.myEncrypt import HashCipher
from utils.myEnum import SystemDelEnum, SystemStatusEnum
from utils.myResFormat import ResultJson, ResultCode
from utils.myTimeFormat import MyTimeUtils
from web.captchaImage import CaptchaImage
from web.models import SystemUser, SystemUserRole, SystemRole, SystemRoleMenu, SystemMenu
from web.serializer import SystemUserSerializer, SystemMenuSerializer, SystemRoleSerializer

RedisClient = get_redis_connection()


class CaptchaImageView(APIView):

    def get(self, request, *args, **kwargs):
        """【系统用户】获取验证码"""
        captcha = CaptchaImage()

        # 生成验证码图片和字符串
        captcha_string, image_base64 = captcha.generate(width=120, height=40)

        res = Dict()
        uid = uuid.uuid4().hex
        res.img = image_base64
        res.uuid = uid
        res.captchaEnabled = True

        RedisClient.set(uid, captcha_string, ex=5 * 60)

        return JsonResponse(ResultJson(ResultCode.SUCCESS, data=res.to_dict()).result)


class LoginView(APIView):
    "登录"

    def post(self, request, *args, **kwargs):

        username = request.data.get("username", "")
        password = request.data.get("password", "")

        # 如果有验证码的情况,校验方式
        uid = request.data.get("uuid", "")
        code = request.data.get("code", "")

        # 密码加密
        password = HashCipher.md5(config.ENCRYPT_STRING + str(password))

        if uid:
            authCode = RedisClient.get(uid)
            if not authCode:
                return JsonResponse(ResultJson(ResultCode.AUTH_CODE_EXP).result)
            else:
                if str(authCode).strip() != str(code).strip():
                    return JsonResponse(ResultJson(ResultCode.AUTH_CODE_ERROR).result)

        Users = SystemUser.objects.filter(username=username, password=password)
        if not Users:
            return JsonResponse(ResultJson(ResultCode.PASSWORD_ERROR).result)

        User = Users.first()
        user_data = SystemUserSerializer(instance=User).data

        # 用户是否被删除
        if User.delFlag == SystemDelEnum.p1.value:
            return JsonResponse(ResultJson(ResultCode.USER_NOT_EXIST).result)

        # 用户是否被禁用
        if User.status == SystemStatusEnum.p1.value:
            return JsonResponse(ResultJson(ResultCode.USER_NOT_ALLOW).result)

        # 更新用户的登陆信息
        User.loginIp = request.META.get("REMOTE_ADDR", "")
        User.loginDate = MyTimeUtils.TimeFormat()
        User.save()

        # 获取角色信息
        token = uuid.uuid4().hex
        userInfo = Dict()

        # 找到用户id和角色的映射
        UserRoleMap = SystemUserRole.objects.filter(userId=User.userId)

        RoleDataList = SystemRole.objects.filter(roleId__in=[roleItem.roleId for roleItem in UserRoleMap], delFlag=SystemDelEnum.p0.value,
                                                 status=SystemStatusEnum.p0.value)

        userInfo.user = user_data
        userInfo.roles = [role.roleKey for role in RoleDataList]
        user_data["role"] = SystemRoleSerializer(instance=RoleDataList, many=True).data

        if any([role.roleAdmin for role in RoleDataList]):
            userInfo.permissions = ["*:*:*"]
        else:

            roleIds = list(set([item.roleId for item in RoleDataList]))

            # 对目录权限进行去重
            RoleMenus = SystemRoleMenu.objects.filter(roleId__in=roleIds)

            menuIds = list(set([item.menuId for item in RoleMenus]))

            Menus = SystemMenu.objects.filter(menuId__in=menuIds, status=SystemStatusEnum.p0.value)

            userInfo.permissions = [item.perms for item in Menus]

        RedisClient.set(token, json.dumps(userInfo.to_dict()), ex=60 * 60)

        return JsonResponse(ResultJson(ResultCode.SUCCESS, data=token).result)


class LogoutView(APIView):
    "退出登录"

    def post(self, request, *args, **kwargs):
        token = request.headers.user_info.get("token")

        # token不存在的情况
        if not token:
            return JsonResponse(ResultJson(ResultCode.SUCCESS).result)

        RedisClient.delete(token)
        return JsonResponse(ResultJson(ResultCode.SUCCESS).result)


class GetInfoView(APIView):
    "获取登陆信息"

    def get(self, request, *args, **kwargs):
        user_info = request.headers.user_info
        return JsonResponse(ResultJson(ResultCode.SUCCESS, data=user_info).result)


class GetRoutersView(APIView):
    "获取用户权限路由"

    def routerFormat(self, MenuData):
        # 目录数据组装前端的路由格式
        container = []
        for item in MenuData:
            # 组装目录
            if item.get('menuType') == 'M':

                # 判断是否外链接
                if item.get('isFrame') == "0":
                    menuItem = {"id": item.get('menuId'), "parentId": item.get('parentId'), "component": "Layout", "hidden": bool(int(item.get('visible'))),
                                "path": item.get('path'), "name": item.get('path'),
                                "meta": {"icon": item.get('icon'), "link": item.get('path'), "noCache": bool(int(item.get('isCache'))),
                                         "title": item.get('menuName'), }

                                }
                else:
                    menuItem = {"id": item.get('menuId'), "parentId": item.get('parentId'), "component": "Layout", "hidden": bool(int(item.get('visible'))),
                                "path": "/" + item.get('path'), "name": str(item.get('path')).capitalize(), "redirect": "noRedirect",
                                "meta": {"icon": item.get('icon'), "link": "", "noCache": bool(int(item.get('isCache'))), "title": item.get('menuName'), }}
                container.append(menuItem)

            # 处理组件形式
            elif item.get('menuType') == 'C':
                menuItem = {"id": item.get('menuId'), "parentId": item.get('parentId'), "component": item.get('component'),
                            "hidden": bool(int(item.get('visible'))), "path": item.get('path'), "name": str(item.get('path')).capitalize(),
                            "redirect": "noRedirect",
                            "meta": {"icon": item.get('icon'), "link": "", "noCache": bool(int(item.get('isCache'))), "title": item.get('menuName'), }}
                container.append(menuItem)

        # 基础数据组装后，组装成树结构
        treeData = TreeBuilder(container).build(parentKey="parentId", ownerKey="id", topParent="0")
        return list(treeData.values()) if treeData else []

    def get(self, request, *args, **kwargs):

        user_info = request.headers.user_info

        # 获取用户的角色信息
        roleData = user_info.get("user", {}).get("role", [])
        roleAdminList = [roleItem.get("roleAdmin") for roleItem in roleData]

        if any(roleAdminList):
            Menus = SystemMenu.objects.all()
        else:
            roleIds = list(set([item.get("roleId") for item in roleData]))

            # 对目录权限进行去重
            RoleMenus = SystemRoleMenu.objects.filter(roleId__in=roleIds)

            menuIds = list(set([item.menuId for item in RoleMenus]))

            Menus = SystemMenu.objects.filter(menuId__in=menuIds, status=SystemStatusEnum.p0.value)

        MenuData = SystemMenuSerializer(instance=Menus, many=True).data
        routerInfo = self.routerFormat(MenuData)
        return JsonResponse(ResultJson(ResultCode.SUCCESS, data=routerInfo).result)
