# -*- coding: utf-8 -*-
"""
@Author ：mengying
@Date   ：2024/5/31 17:17
@Email  : 652044581@qq.com
@Desc   : 初始化数据
"""
import django
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'application.settings')
django.setup()

import logging
from utils.mySnowflake import Sf
from web.models import SystemInit
from web.models import SystemDept, SystemRole, SystemUser, SystemMenu, SystemUserRole
from utils.myEnum import SystemUserTypeEnum
from config import config
from utils.myEncrypt import HashCipher

logger = logging.getLogger("django")


class DatabaseUtils(object):
    REDIS_KEY = 'init_database'

    @classmethod
    def init_database(cls):
        """初始化数据库"""

        # 多节点初始化
        hasInit: bool = cls.initFlag()
        deptId = Sf.generate()
        roleId = Sf.generate()
        userId = Sf.generate()

        if not hasInit:
            cls.initDept(deptId)
            cls.initRole(roleId)
            cls.initUser(userId)
            cls.initUserRole(userId, roleId)
            cls.initMenu()

        logger.info("init database successfully")

    @classmethod
    def initDept(cls, deptId):
        initDeptData = {"createBy": "superAdmin", "deptId": deptId, "ancestors": "0", "parentId": "0", "deptName": "重庆亲笔签数字科技有限公司", "orderNum": 0,
            "leader": "admin", "phone": "17783098377", "email": "652044581@qq.com", "status": "0", "delFlag": "0", }
        SystemDept(**initDeptData).save()

    @classmethod
    def initRole(cls, roleId):
        """初始化角色超级管理员"""
        initRoleData = {"createBy": "superAdmin", "roleId": roleId, "roleName": "超级管理员", "roleAdmin": True, "roleKey": "superAdmin", "roleSort": "0",
            "status": "0", "delFlag": "0", }
        SystemRole(**initRoleData).save()

    @classmethod
    def initUser(cls, userId):
        initUserData = {"userId": userId, "username": "superAdmin", "nickName": "superAdmin", "password": HashCipher.md5(config.ENCRYPT_STRING + "superAdmin"),
                        "phone": "17783098375", "email": "652044581@qq.com", "status": "0", "userType": SystemUserTypeEnum.p1.value}
        SystemUser(**initUserData).save()

    @classmethod
    def initUserRole(cls, userId, roleId):
        """初始化用户角色关系"""
        initUserRoleData = {"userId": userId, "roleId": roleId}
        SystemUserRole(**initUserRoleData).save()

    @classmethod
    def initMenu(cls, ):
        """初始化前端菜单"""
        menuParentId = Sf.generate()
        menuUserId = Sf.generate()
        menuRoleId = Sf.generate()
        menuMenuId = Sf.generate()
        menuDeptId = Sf.generate()
        initMenuData = [
            {"menuId": menuParentId, "menuName": "系统管理", "parentId": "0", "orderNum": 3, "path": "system", "component": "", "perms": "", "query": "",
                "menuType": "M", "icon": "system", },
            {"menuId": menuUserId, "menuName": "用户管理", "parentId": menuParentId, "orderNum": 1, "path": "user", "component": "system/user/index",
                "perms": "system:user:list", "query": "", "menuType": "C", "icon": "user", },

            {"menuId": menuRoleId, "menuName": "角色管理", "parentId": menuParentId, "orderNum": 2, "path": "role", "component": "system/role/index",
                "perms": "system:role:list", "query": "", "menuType": "C", "icon": "peoples", },
            {"menuId": menuMenuId, "menuName": "菜单管理", "parentId": menuParentId, "orderNum": 3, "path": "menu", "component": "system/menu/index",
                "perms": "system:menu:list", "query": "", "menuType": "C", "icon": "tree-table", },
            {"menuId": menuDeptId, "menuName": "部门管理", "parentId": menuParentId, "orderNum": 4, "path": "dept", "component": "system/dept/index",
                "perms": "system:dept:list", "query": "", "menuType": "C", "icon": "tree", },
            {"menuId": Sf.generate(), "menuName": "用户查询", "parentId": menuUserId, "orderNum": 1, "path": "", "component": "", "perms": "system:user:query",
                "query": "", "menuType": "F", "icon": "#", },
            {"menuId": Sf.generate(), "menuName": "用户新增", "parentId": menuUserId, "orderNum": 2, "path": "", "component": "", "perms": "system:user:add",
                "query": "", "menuType": "F", "icon": "#", },
            {"menuId": Sf.generate(), "menuName": "用户修改", "parentId": menuUserId, "orderNum": 3, "path": "", "component": "", "perms": "system:user:edit",
                "query": "", "menuType": "F", "icon": "#", },
            {"menuId": Sf.generate(), "menuName": "用户删除", "parentId": menuUserId, "orderNum": 4, "path": "", "component": "", "perms": "system:user:remove",
                "query": "", "menuType": "F", "icon": "#", },

            {"menuId": Sf.generate(), "menuName": "角色查询", "parentId": menuRoleId, "orderNum": 1, "path": "", "component": "", "perms": "system:role:query",
                "query": "", "menuType": "F", "icon": "#", },
            {"menuId": Sf.generate(), "menuName": "角色新增", "parentId": menuRoleId, "orderNum": 2, "path": "", "component": "", "perms": "system:role:add",
                "query": "", "menuType": "F", "icon": "#", },
            {"menuId": Sf.generate(), "menuName": "角色修改", "parentId": menuRoleId, "orderNum": 3, "path": "", "component": "", "perms": "system:role:edit",
                "query": "", "menuType": "F", "icon": "#", },
            {"menuId": Sf.generate(), "menuName": "角色删除", "parentId": menuRoleId, "orderNum": 4, "path": "", "component": "", "perms": "system:role:remove",
                "query": "", "menuType": "F", "icon": "#", },

            {"menuId": Sf.generate(), "menuName": "菜单查询", "parentId": menuMenuId, "orderNum": 1, "path": "", "component": "", "perms": "system:menu:query",
                "query": "", "menuType": "F", "icon": "#", },
            {"menuId": Sf.generate(), "menuName": "菜单新增", "parentId": menuMenuId, "orderNum": 2, "path": "", "component": "", "perms": "system:menu:add",
                "query": "", "menuType": "F", "icon": "#", },
            {"menuId": Sf.generate(), "menuName": "菜单修改", "parentId": menuMenuId, "orderNum": 3, "path": "", "component": "", "perms": "system:menu:edit",
                "query": "", "menuType": "F", "icon": "#", },
            {"menuId": Sf.generate(), "menuName": "菜单删除", "parentId": menuMenuId, "orderNum": 4, "path": "", "component": "", "perms": "system:menu:remove",
                "query": "", "menuType": "F", "icon": "#", },

            {"menuId": Sf.generate(), "menuName": "部门查询", "parentId": menuDeptId, "orderNum": 1, "path": "", "component": "", "perms": "system:dept:query",
                "query": "", "menuType": "F", "icon": "#", },
            {"menuId": Sf.generate(), "menuName": "部门新增", "parentId": menuDeptId, "orderNum": 2, "path": "", "component": "", "perms": "system:dept:add",
                "query": "", "menuType": "F", "icon": "#", },
            {"menuId": Sf.generate(), "menuName": "部门修改", "parentId": menuDeptId, "orderNum": 3, "path": "", "component": "", "perms": "system:dept:edit",
                "query": "", "menuType": "F", "icon": "#", },
            {"menuId": Sf.generate(), "menuName": "部门删除", "parentId": menuDeptId, "orderNum": 4, "path": "", "component": "", "perms": "system:dept:remove",
                "query": "", "menuType": "F", "icon": "#", }, ]
        for item in initMenuData:
            SystemMenu(**item).save()

    @classmethod
    def initFlag(cls):
        """防止多次初始化文件"""
        init = SystemInit.objects.all()
        if not init:
            SystemInit(Init=True).save()
            return False
        else:
            return True


DatabaseUtils.init_database()
