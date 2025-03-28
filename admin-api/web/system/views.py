import json
from functools import wraps

from addict import Dict
from django.db.models import Q
from django.http.response import JsonResponse
from django_redis import get_redis_connection
from rest_framework.request import Request
from rest_framework.views import APIView

from config import config
from utils.myDataUtils import TreeBuilder
from utils.myEncrypt import HashCipher
from utils.myEnum import SystemDelEnum, SystemStatusEnum, SystemUserTypeEnum
from utils.myResFormat import ResultJson, ResultCode
from utils.mySnowflake import Sf
from web.models import SystemDept, SystemUser, SystemRole, SystemUserRole, SystemMenu, SystemRoleMenu
from web.paginator import StandardResultsSetPagination
from web.serializer import SystemDeptSerializer, SystemUserSerializer, SystemRoleSerializer, SystemMenuSerializer

RedisClient = get_redis_connection()


# 检验权限字符串的装饰器
def permAuth(perKey):
    def decorator(function):
        @wraps(function)
        def decorated_function(self, *args, **kwargs):
            # 获取token中的用户权限
            user_info = {}
            for item in args:
                if isinstance(item, Request):
                    user_info = item.headers.user_info
            user_permissions = user_info.get("permissions", [])

            # 判断是否有权限
            if "*:*:*" in user_permissions or perKey in user_permissions:
                response = function(self, *args, **kwargs)
                return response
            else:
                return JsonResponse(ResultJson(ret=ResultCode.PRE_AUTH_ERROR).result)

        return decorated_function

    return decorator


def response2json(response) -> dict:
    return json.loads(response.content.decode())


class DeptListView(APIView):
    """【系统部门】列表接口"""

    @permAuth("system:dept:list")
    def get(self, request, *args, **kwargs):
        deptName: str = request.GET.get('deptName')
        status: str = request.GET.get('status')

        q = Q()
        q.connector = 'AND'

        if deptName:
            q.children.append(('deptName', deptName))

        if status:
            q.children.append(('status', status))

        q.children.append(('delFlag', SystemDelEnum.p0.value))

        dept = SystemDept.objects.filter(q)
        deptData = SystemDeptSerializer(instance=dept, many=True).data
        return JsonResponse(ResultJson(ResultCode.SUCCESS, data=deptData).result)


class DeptCreateView(APIView):
    """【系统部门】新增部门"""

    @permAuth("system:dept:add")
    def post(self, request, *args, **kwargs):

        data: dict = request.data

        parentId = request.data.get('parentId')

        dept_obj = SystemDept.objects.filter(deptId=parentId)
        if not dept_obj:
            raise Exception("未找到系统部门父级id")

        dept_obj = dept_obj.first()
        data["ancestors"] = dept_obj.ancestors + "," + dept_obj.deptId
        data["deptId"] = Sf.generate()

        # 判断同一父级部门下不重名
        deptNameExist = SystemDept.objects.filter(deptName=data.get("deptName"), parentId=data.get("parentId"))
        if deptNameExist:
            return JsonResponse(ResultJson(ret=ResultCode.DEPT_ERROR).result)

        SystemDept.objects.create(**data)
        return JsonResponse(ResultJson(ResultCode.SUCCESS, data=data).result)

    @permAuth("system:dept:edit")
    def put(self, request, *args, **kwargs):
        data: dict = request.data
        deptId = data.get('deptId')

        deptData = SystemDept.objects.get(deptId=deptId)

        # 判断原始目录的父级id是否变化
        if deptData.parentId == data.get('parentId'):
            SystemDept.objects.filter(deptId=deptId).update(**data)
        else:
            # 处理本条数据的上级关联关系
            parentId = data.get('parentId')
            parentData = SystemDept.objects.get(deptId=parentId)
            repAncestors = parentData.ancestors + "," + parentId
            data['ancestors'] = repAncestors
            SystemDept.objects.filter(deptId=deptId).update(**data)

            # 处理下级关联的路径问题
            oldAncestors = deptData.ancestors + "," + deptData.deptId
            SystemDeptDataList = SystemDept.objects.filter(ancestors__contains=oldAncestors, delFlag=SystemDelEnum.p0.value)
            for item in SystemDeptDataList:
                new_ancestors = item.ancestors
                new_ancestors = str(new_ancestors).replace(oldAncestors, repAncestors + "," + deptData.deptId)
                item.ancestors = new_ancestors
                item.save()
        return JsonResponse(ResultJson(ret=ResultCode.SUCCESS).result)


class DeptDetailView(APIView):
    """【系统部门】新增部门"""

    @permAuth("system:dept:query")
    def get(self, request, deptId, *args, **kwargs):
        """【系统部门】部门详情"""
        data = SystemDept.objects.get(deptId=deptId, delFlag=SystemDelEnum.p0.value)
        ser = SystemDeptSerializer(instance=data)
        return JsonResponse(ResultJson(ResultCode.SUCCESS, data=ser.data).result)

    @permAuth("system:dept:remove")
    def delete(self, request, deptId, *args, **kwargs):
        # 更新部门状态
        SystemDept.objects.filter(deptId=deptId).update(delFlag=SystemDelEnum.p1.value)

        # 更新人员绑定部门
        SystemUser.objects.filter(deptId=deptId).update(deptId="")
        return JsonResponse(ResultJson(ret=ResultCode.SUCCESS).result)


class DeptExcludeView(APIView):
    """【系统部门】排除查询"""

    @permAuth("system:dept:query")
    def get(self, request, deptId, *args, **kwargs):
        # 查询部门id不是指定id或者ancestors不包含该id,且状态未删除的数据
        userData = SystemDept.objects.filter(delFlag=SystemDelEnum.p0.value, status=SystemStatusEnum.p0.value).exclude(deptId=deptId,
                                                                                                                       ancestors__contains=deptId)
        ser = SystemDeptSerializer(instance=userData, many=True)
        return JsonResponse(ResultJson(ResultCode.SUCCESS, data=ser.data).result)


class RoleListView(APIView):
    """【系统角色】列表接口"""
    @permAuth("system:role:query")
    def get(self, request, *args, **kwargs):
        roleName: str = request.GET.get('roleName')
        roleKey: str = request.GET.get('roleKey')
        status: str = request.GET.get('status')

        q = Q()
        q.connector = 'AND'

        if roleName:
            q.children.append(('roleName', roleName))

        if roleKey:
            q.children.append(('roleKey', roleKey))

        if status:
            q.children.append(('status', status))

        q.children.append(('roleAdmin', False))
        q.children.append(('delFlag', SystemDelEnum.p0.value))

        roleData = SystemRole.objects.filter(q).order_by('roleSort')

        paginator = StandardResultsSetPagination()
        role_list = paginator.paginate_queryset_count(roleData, self.request, view=self, serializer=SystemRoleSerializer)

        return JsonResponse(ResultJson(ResultCode.SUCCESS, data=role_list).result)


class RoleCreateView(APIView):
    """【系统角色】新增接口"""
    @permAuth("system:role:add")
    def post(self, request, *args, **kwargs):
        data: dict = request.data
        roleKey = data.get("roleKey")
        roleName = data.get("roleName")
        menuIds = data.pop("menuIds", [])
        roleId = Sf.generate()
        data["roleId"] = roleId

        roleData = SystemRole.objects.filter(Q(roleKey=roleKey, delFlag=SystemDelEnum.p0.value) | Q(roleName=roleName, delFlag=SystemDelEnum.p0.value))

        if roleData:
            return JsonResponse(ResultJson(ret=ResultCode.ROLE_ERROR).result)

        # 删除原始的关系
        SystemRoleMenu.objects.filter(roleId=roleId).delete()
        for menuId in menuIds:
            SystemRoleMenu.objects.create(menuId=menuId, roleId=roleId)

        # 创建角色数据
        SystemRole.objects.create(**data)
        return JsonResponse(ResultJson(ret=ResultCode.SUCCESS).result)

    @permAuth("system:role:edit")
    def put(self, request, *args, **kwargs):
        data: dict = request.data
        roleId = data.get("roleId")
        menuIds = data.pop("menuIds", [])
        roleAdmin = data.pop("roleAdmin", False)

        # 删除原始的关系
        SystemRoleMenu.objects.filter(roleId=roleId).delete()
        for menuId in menuIds:
            SystemRoleMenu.objects.create(menuId=menuId, roleId=roleId)

        # 更新角色数据
        SystemRole.objects.filter(roleId=roleId).update(**data)
        return JsonResponse(ResultJson(ret=ResultCode.SUCCESS).result)


class RoleStatusView(APIView):
    """【系统角色】修改状态"""
    @permAuth("system:role:edit")
    def put(self, request):
        data: dict = request.data
        roleId = data.get("roleId")
        SystemRole.objects.filter(roleId=roleId).update(**data)
        return JsonResponse(ResultJson(ret=ResultCode.SUCCESS).result)


class RoleDetailView(APIView):
    @permAuth("system:role:query")
    def get(self, request, roleId: str):
        """【系统角色】获取角色信息"""

        roleData = SystemRole.objects.get(roleId=roleId)
        roleData = SystemRoleSerializer(instance=roleData).data

        return JsonResponse(ResultJson(ret=ResultCode.SUCCESS, data=roleData).result)

    @permAuth("system:role:remove")
    def delete(self, request, roleId: str):
        """【系统角色】获取删除角色信息"""

        roleIds = roleId.split(',')
        SystemRole.objects.filter(roleId__in=roleIds).update(delFlag=SystemDelEnum.p1.value)

        SystemUserRole.objects.filter(roleId__in=roleIds).delete()

        return JsonResponse(ResultJson(ret=ResultCode.SUCCESS).result)


class AuthUserCancelView(APIView):
    def put(self, request):
        """【系统角色】取消角色人员授权"""
        # 处理角色用户关系
        roleId: str = request.data.get('roleId')
        userId: str = request.data.get('userId')

        # 判断是批量删除还是单个删除
        SystemUserRole.objects.filter(roleId=roleId, userId=userId).delete()
        return JsonResponse(ResultJson(ret=ResultCode.SUCCESS).result)


class AuthUserAllocatedListView(APIView):

    def get(self, request):
        """【系统角色】给角色分配人员"""
        roleId: str = request.GET.get('roleId')
        username: str = request.GET.get('username')
        phone: str = request.GET.get('phone')

        UserRoleIds = SystemUserRole.objects.filter(roleId=roleId)

        q = Q()
        q.connector = 'AND'

        if username:
            q.children.append(('username', username))

        if phone:
            q.children.append(('phone', phone))

        q.children.append(('userId__in', [item.userId for item in UserRoleIds]))
        q.children.append(('delFlag', SystemDelEnum.p0.value))
        q.children.append(('userType', SystemUserTypeEnum.p0.value))

        userData = SystemUser.objects.filter(q)

        paginator = StandardResultsSetPagination()

        # 组装人员的部门信息
        userData = paginator.paginate_queryset_count(userData, self.request, view=self, serializer=SystemUserSerializer)
        for item in userData.get("data", []):
            deptId = item.get('deptId')
            if not deptId:
                item["dept"] = {}
            else:
                deptData = SystemDept.objects.get(deptId=deptId)
                item["dept"] = SystemDeptSerializer(instance=deptData).data

        return JsonResponse(ResultJson(ret=ResultCode.SUCCESS, data=userData).result)


class AuthUserUnallocatedListView(APIView):

    def get(self, request):
        """【系统角色】获取未授权用户列表"""
        roleId: str = request.GET.get('roleId')
        username: str = request.GET.get('username')
        phone: str = request.GET.get('phone')

        UserRoleIds = SystemUserRole.objects.filter(roleId=roleId)

        q = Q()
        q.connector = 'AND'

        if username:
            q.children.append(('username', username))

        if phone:
            q.children.append(('phone', phone))

        q.children.append(('delFlag', SystemDelEnum.p0.value))
        q.children.append(('userType', SystemUserTypeEnum.p0.value))

        userData = SystemUser.objects.filter(q).exclude(userId__in=[item.userId for item in UserRoleIds])

        paginator = StandardResultsSetPagination()

        # 组装人员的部门信息
        userData = paginator.paginate_queryset_count(userData, self.request, view=self, serializer=SystemUserSerializer)
        for item in userData.get("data", []):
            deptId = item.get('deptId')
            if not deptId:
                item["dept"] = {}
            else:
                deptData = SystemDept.objects.get(deptId=deptId)
                item["dept"] = SystemDeptSerializer(instance=deptData).data

        return JsonResponse(ResultJson(ret=ResultCode.SUCCESS, data=userData).result)


class AuthUserSelectAllView(APIView):
    def put(self, request):
        """【系统角色】批量绑定角色人员"""
        roleId: str = request.GET.get('roleId')
        userIds: str = request.GET.get('userIds')
        userIdList = userIds.split(',')

        # 批量插入用户关系
        for userId in userIdList:
            SystemUserRole.objects.create(**dict(userId=userId, roleId=roleId))
        return JsonResponse(ResultJson(ret=ResultCode.SUCCESS).result)


class AuthUserCancelAllView(APIView):
    def put(self, request):
        """【系统角色】批量取消角色人员授权"""
        # 处理角色用户关系
        roleId: str = request.data.get('roleId')
        userIds: str = request.data.get('userIds')
        userIdList = userIds.split(',')

        # 判断是批量删除还是单个删除
        SystemUserRole.objects.filter(roleId=roleId, userId__in=userIdList).delete()

        return JsonResponse(ResultJson(ret=ResultCode.SUCCESS).result)


class UserListView(APIView):
    """【系统用户】列表接口"""

    @permAuth("system:user:list")
    def get(self, request):

        deptId: str = request.GET.get('deptId')
        username: str = request.GET.get('username')
        phone: str = request.GET.get('phone')
        status: str = request.GET.get('status')

        q = Q()
        q.connector = 'AND'

        if deptId:
            deptData = SystemDept.objects.filter(ancestors__contains=deptId)
            deptIds = [item.deptId for item in deptData]
            deptIds.append(deptId)
            q.children.append(('deptId__in', deptIds))

        if username:
            q.children.append(('username', username))

        if phone:
            q.children.append(('phone', phone))

        if status:
            q.children.append(('status', status))

        q.children.append(('delFlag', SystemDelEnum.p0.value))
        q.children.append(('userType', SystemUserTypeEnum.p0.value))

        userData = SystemUser.objects.filter(q)

        # 分页
        paginator = StandardResultsSetPagination()
        userData = paginator.paginate_queryset_count(userData, self.request, view=self, serializer=SystemUserSerializer)

        # 组装人员的部门信息
        for item in userData.get("data", []):
            deptId = item.get('deptId')
            if not deptId:
                item["dept"] = {}
            else:
                deptData = SystemDept.objects.get(deptId=deptId)
                item["dept"] = SystemDeptSerializer(instance=deptData).data

        return JsonResponse(ResultJson(ret=ResultCode.SUCCESS, data=userData).result)


class UserDeptTreeView(APIView):
    """【系统用户】部门的结构树"""

    @classmethod
    def deptFormat(cls, SystemDeptList):
        container = []
        for item in SystemDeptList:
            deptItem = {"id": item.get("deptId"), "parentId": item.get("parentId"), "label": item.get("deptName"), }
            container.append(deptItem)
        return container

    def get(self, request):
        # 查询全部数据
        deptData = SystemDept.objects.filter(delFlag=SystemDelEnum.p0.value, status=SystemStatusEnum.p0.value)

        # 组装前端所需要的数据结构
        SystemDeptList = SystemDeptSerializer(instance=deptData, many=True)
        DeptList = self.deptFormat(SystemDeptList.data)

        # 组装成树的结构
        TreeData = TreeBuilder(DeptList).build(parentKey="parentId", ownerKey="id", topParent="0")
        TreeDataList = list(TreeData.values())

        return JsonResponse(ResultJson(ret=ResultCode.SUCCESS, data=TreeDataList).result)


class UserStatusView(APIView):
    """【系统用户】修改用户状态"""

    @permAuth("*:*:*")
    def put(self, request):
        data: dict = request.data
        userId = data.get("userId")
        SystemUser.objects.filter(userId=userId).update(**data)

        return JsonResponse(ResultJson(ret=ResultCode.SUCCESS).result)


class UserCreateView(APIView):
    """【系统用户】新增接口"""

    @permAuth("*:*:*")
    def post(self, request):
        data: dict = request.data
        username = data.get("username")
        password = data.get('password', "")

        userId = Sf.generate()

        # 判断用户名是否重复
        userExist = SystemUser.objects.filter(username=username, delFlag=SystemDelEnum.p0.value)
        if userExist:
            return JsonResponse(ResultJson(ret=ResultCode.USER_ERROR).result)

        # 处理角色用户关系
        roleIds = data.pop("roleIds", [])
        for roleId in roleIds:
            SystemUserRole.objects.create(**dict(roleId=roleId, userId=userId))

        # 用户表插入数据
        user_info = request.headers.user_info
        username = user_info.get('user', {}).get('username')
        data["userId"] = userId
        data["createBy"] = username
        data["password"] = HashCipher.md5(config.ENCRYPT_STRING + password)
        SystemUser.objects.create(**data)
        return JsonResponse(ResultJson(ret=ResultCode.SUCCESS).result)

    @permAuth("*:*:*")
    def put(self, request):
        """【系统用户】修改信息"""
        # 处理角色用户关系
        data: dict = request.data

        userId = data.get('userId')
        roleIds = data.pop("roleIds", [])

        # 删除以前的角色人员关系，在增加新的关系
        SystemUserRole.objects.filter(userId=userId).delete()
        for roleId in roleIds:
            SystemUserRole.objects.create(**dict(roleId=roleId, userId=userId))

        SystemUser.objects.filter(userId=userId).update(**data)
        return JsonResponse(ResultJson(ret=ResultCode.SUCCESS).result)

    @permAuth("*:*:*")
    def get(self, request):
        """【系统用户】获取现有的角色列表"""
        res = Dict()
        roleData = SystemRole.objects.filter(status=SystemStatusEnum.p0.value, delFlag=SystemDelEnum.p0.value, roleAdmin=False)
        res.roles = SystemRoleSerializer(instance=roleData, many=True).data
        return JsonResponse(ResultJson(ret=ResultCode.SUCCESS, data=res).result)


class UserDetailView(APIView):
    @permAuth("system:user:query")
    def get(self, request, userId: str):
        """【系统用户】获取用户信息"""
        res = Dict()

        # 找到用户绑定的角色id
        userData = SystemUser.objects.get(userId=userId)

        userRoleData = SystemUserRole.objects.filter(userId=userId)
        roleIds = [item.roleId for item in userRoleData]
        roleData = SystemRole.objects.filter(status=SystemStatusEnum.p0.value, roleAdmin=False, delFlag=SystemDelEnum.p0.value)

        # 组装数据
        res.user = SystemUserSerializer(instance=userData).data
        res.roleIds = roleIds
        res.roles = SystemRoleSerializer(instance=roleData, many=True).data
        return JsonResponse(ResultJson(ret=ResultCode.SUCCESS, data=res).result)

    @permAuth("system:user:remove")
    def delete(self, request, userId: str):
        """【系统用户】获取删除用户信息"""

        # 分割路径的userId,变为list
        userIds = userId.split(',')
        SystemUser.objects.filter(userId__in=userIds).update(delFlag=SystemDelEnum.p1.value)
        return JsonResponse(ResultJson(ret=ResultCode.SUCCESS).result)


class UserProfileView(APIView):

    def get(self, request):
        """【个人中心】获取信息"""
        user_info = request.headers.user_info
        return JsonResponse(ResultJson(ret=ResultCode.SUCCESS, data=user_info).result)

    def put(self, request):
        """【个人中心】修改"""
        data: dict = request.data
        user_info = request.headers.user_info
        userId = user_info.get('user', {}).get('userId')
        SystemUser.objects.filter(userId=userId).update(**data)
        return JsonResponse(ResultJson(ret=ResultCode.SUCCESS).result)


class UserProfileAvatarView(APIView):

    def post(self, request):
        """【个人中心】修改头像"""
        avatar = request.Files.get("avatarfile")
        user_info = request.headers.user_info
        userId = user_info.get('user', {}).get('userId')

        # TODO: 上传头像文件流，生成一个url，更新用户信息的头像字段（没有obs， 功能未作）

        return JsonResponse(ResultJson(ret=ResultCode.SUCCESS, data=user_info).result)


class UserResetPwdView(APIView):
    @permAuth("*:*:*")
    def put(self, request):
        """【系统用户】重置密码/ 需要管理员权限"""
        data: dict = request.data
        password = data.get('password')
        userId = data.get('userId')

        # 修改密码
        password_md5 = HashCipher.md5(config.ENCRYPT_STRING + password)

        SystemUser.objects.filter(userId=userId).update(password=password_md5)
        return JsonResponse(ResultJson(ret=ResultCode.SUCCESS).result)


class UserUpdatePwdView(APIView):
    def put(self, request):
        """【系统用户】更新密码"""
        oldPassword = request.GET.get('oldPassword')
        newPassword = request.GET.get('newPassword')

        # 判断旧密码是否正确
        user_info = request.headers.user_info
        userId = user_info.get('user', {}).get('userId', "")

        # 对密码进行加密
        old_encrypt_password = HashCipher.md5(config.ENCRYPT_STRING + str(oldPassword))
        new_encrypt_password = HashCipher.md5(config.ENCRYPT_STRING + str(newPassword))

        userData = SystemUser.objects.filter(password=old_encrypt_password, userId=userId)

        if not userData:
            return JsonResponse(ResultJson(ret=ResultCode.PASSWORD_ERROR).result)
        else:

            SystemUser.objects.filter(userId=userId).update(password=new_encrypt_password)
            return JsonResponse(ResultJson(ret=ResultCode.SUCCESS).result)


class AuthRoleView(APIView):

    def get(self, request, userId: str):
        """【系统用户】查询角色映射关系"""
        # 查询用户信息
        userData = SystemUser.objects.get(userId=userId)

        # 查询用户角色映射关系
        userRoleList = SystemUserRole.objects.filter(userId=userId)

        # 查询角色信息
        roleIds = [item.roleId for item in userRoleList]

        # 查询全部角色信息过滤超级管理员
        roleData = SystemRole.objects.filter(roleAdmin=False)

        # 序列化
        userData = SystemUserSerializer(instance=userData).data
        roleData = SystemRoleSerializer(instance=roleData, many=True).data

        # 找到过滤的角色
        for role in roleData:
            role['flag'] = True if role.get("roleId") in roleIds else False

        # 组装返回数据
        resData = dict(user=userData, roles=roleData)
        return JsonResponse(ResultJson(ret=ResultCode.SUCCESS, data=resData).result)

    def put(self, request):
        """【系统用户】修改角色映射关系"""
        userId = request.GET.get("userId")
        roleIds = request.GET.get("roleIds")
        roleIds = roleIds.split(",")

        # 删除以前的角色人员关系，在增加新的关系
        SystemUserRole.objects.filter(userId=userId).delete()
        for roleId in roleIds:
            SystemUserRole.objects.create(**dict(roleId=roleId, userId=userId))

        return JsonResponse(ResultJson(ret=ResultCode.SUCCESS, data=None).result)


class MenuDetailView(APIView):
    @permAuth("system:menu:query")
    def get(self, request, menuId: str):
        """【系统用户】查询"""
        menuData = SystemMenu.objects.get(menuId=menuId)
        menuData = SystemMenuSerializer(instance=menuData).data
        return JsonResponse(ResultJson(ret=ResultCode.SUCCESS, data=menuData).result)

    @permAuth("system:menu:remove")
    def delete(self, request, menuId: str):
        """【系统用户】删除"""

        # 删除目录信息
        SystemMenu.objects.filter(menuId=menuId).delete()

        # 删除角色目录映射
        SystemRoleMenu.objects.filter(menuId=menuId).delete()
        return JsonResponse(ResultJson(ret=ResultCode.SUCCESS).result)


class MenuListView(APIView):

    @permAuth("system:menu:list")
    def get(self, request):
        """【系统目录】列表"""
        menuName: str = request.GET.get('menuName')
        status: str = request.GET.get('status')

        q = Q()
        q.connector = 'AND'

        if menuName:
            q.children.append(('menuName', menuName))

        if status:
            q.children.append(('status', status))

        q.children.append(('visible', SystemDelEnum.p0.value))

        # 查询数据列表
        menuData = SystemMenu.objects.filter(q).order_by('orderNum')
        menuData = SystemMenuSerializer(instance=menuData, many=True).data

        return JsonResponse(ResultJson(ret=ResultCode.SUCCESS, data=menuData).result)


class MenuCreateView(APIView):

    @permAuth("system:menu:add")
    def post(self, request):
        """【系统目录】新增"""
        data: dict = request.data
        parentId = data.get("parentId")
        menuName = data.get("menuName")
        # 生成父级数据
        data["menuId"] = Sf.generate()

        menuExist = SystemMenu.objects.filter(parentId=parentId, menuName=menuName)

        if menuExist:
            return JsonResponse(ResultJson(ret=ResultCode.MENU_ERROR).result)

        SystemMenu.objects.create(**data)

        return JsonResponse(ResultJson(ret=ResultCode.SUCCESS, data=data).result)

    @permAuth("system:menu:edit")
    def put(self, request):
        """【系统目录】修改"""

        data: dict = request.data
        menuId = data.get('menuId')
        SystemMenu.objects.filter(menuId=menuId).update(**data)
        return JsonResponse(ResultJson(ret=ResultCode.SUCCESS).result)


class MenuTreeSelectView(APIView):
    """【系统目录】树选择"""

    @classmethod
    def MenuFormat(cls, MenuData):
        container = []
        for item in MenuData:
            deptItem = {"id": item.get("menuId"), "parentId": item.get("parentId"), "label": item.get("menuName"), }
            container.append(deptItem)
        return container

    def get(self, request):
        menuData = SystemMenu.objects.filter(status=SystemStatusEnum.p0.value)
        menuData = SystemMenuSerializer(instance=menuData, many=True).data

        # 组装前端所需要的数据结构
        MenuList = self.MenuFormat(menuData)

        # 组装成树的结构
        TreeData = TreeBuilder(MenuList).build(parentKey="parentId", ownerKey="id", topParent="0")
        TreeDataList = list(TreeData.values())
        return JsonResponse(ResultJson(ret=ResultCode.SUCCESS, data=TreeDataList).result)


class MenuRoleTreeSelectView(APIView):
    """【系统目录】已经选择树选择器"""

    def get(self, request, roleId: str):
        res = Dict()

        # 查询树的列表
        TreeDataListResponse = MenuTreeSelectView().get(request)
        TreeDataList = response2json(TreeDataListResponse).get("data", [])

        # 查询选中数据的
        res.menus = TreeDataList
        roleMenuData = SystemRoleMenu.objects.filter(roleId=roleId)

        res.checkedKeys = [item.menuId for item in roleMenuData]
        return JsonResponse(ResultJson(ret=ResultCode.SUCCESS, data=res.to_dict()).result)
