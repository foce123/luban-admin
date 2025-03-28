from django.db import models

from database.core import CoreModel


class SystemInit(CoreModel):
    Init = models.BooleanField(default=False, blank=True, help_text="是否已经初始化数据库")

    class Meta:
        db_table = 'system_init'
        verbose_name = '部门管理'


class SystemDept(CoreModel):
    parentId = models.CharField(max_length=64, default="", verbose_name="父id", help_text="父id")
    deptName = models.CharField(max_length=64, default="", verbose_name="部门名称", help_text="部门名称")
    deptId = models.CharField(unique=True, max_length=64, default="", verbose_name="部门id", help_text="部门id")
    orderNum = models.IntegerField(default=0, verbose_name="排序", help_text="排序")
    leader = models.CharField(max_length=32, default="", verbose_name="负责人", help_text="负责人")
    phone = models.CharField(max_length=32, default="", verbose_name="联系电话", help_text="联系电话")
    email = models.CharField(max_length=32, default="", verbose_name="邮箱", help_text="邮箱")
    status = models.CharField(max_length=4, default="0", verbose_name="启用状态", help_text="启用状态 （0正常 1停用）")
    delFlag = models.CharField(max_length=4, default="0", verbose_name="是否删除", help_text="是否删除 （0存在 2删除）")
    ancestors = models.CharField(max_length=64, default="", verbose_name="上级目录id", help_text="上级目录id")

    class Meta:
        indexes = [models.Index(fields=['deptId'], name='SystemDept_deptId')]
        db_table = 'system_dept'
        verbose_name = '部门管理'


class SystemMenu(CoreModel):
    menuId = models.CharField(unique=True, max_length=64, default="", verbose_name="菜单ID", help_text="菜单ID")
    menuName = models.CharField(max_length=64, default="", verbose_name="菜单名称", help_text="菜单名称")
    parentId = models.CharField(max_length=64, default="", verbose_name="父菜单ID", help_text="父菜单ID")
    orderNum = models.IntegerField(default=0, verbose_name="显示顺序", help_text="显示顺序")
    path = models.CharField(max_length=64, default="", verbose_name="路由地址", help_text="路由地址")
    component = models.CharField(max_length=64, default="", verbose_name="组件路径", help_text="组件路径")
    query = models.CharField(max_length=64, default="", verbose_name="路由参数", help_text="路由参数")
    isFrame = models.CharField(max_length=4, default="1", verbose_name="是否为外链（0是 1否）", help_text="是否为外链（0是 1否）")
    isCache = models.CharField(max_length=4, default="0", verbose_name="是否缓存（0缓存 1不缓存）", help_text="是否缓存（0缓存 1不缓存）")
    visible = models.CharField(max_length=4, default="0", verbose_name="菜单状态（0显示 1隐藏）", help_text="菜单状态（0显示 1隐藏）")
    menuType = models.CharField(max_length=4, default="", verbose_name="菜单类型（M目录 C菜单 F按钮）", help_text="菜单类型（M目录 C菜单 F按钮）")
    status = models.CharField(max_length=4, default="0", verbose_name="菜单状态（0正常 1停用）", help_text="菜单状态（0正常 1停用）")
    perms = models.CharField(max_length=32, default="", verbose_name="权限标识", help_text="权限标识")
    icon = models.CharField(max_length=32, default="", verbose_name="菜单图", help_text="菜单图")

    class Meta:
        db_table = 'system_menu'
        verbose_name = '目录管理'
        indexes = [models.Index(fields=['menuId'], name='SystemMenu_menuId')]


class SystemRole(CoreModel):
    roleId = models.CharField(unique=True, max_length=64, default="", verbose_name="角色id", help_text="角色id")
    roleName = models.CharField(max_length=64, default="", verbose_name="角色名称", help_text="角色名称")
    roleKey = models.CharField(max_length=64, default="", verbose_name="角色权限字符", help_text="角色权限字符")
    roleSort = models.IntegerField(default=0, verbose_name="角色排序", help_text="角色排序")
    roleAdmin = models.BooleanField(max_length=64, default=False, verbose_name="是否是超级管理员", help_text="是否是超级管理员")
    status = models.CharField(max_length=4, default="0", verbose_name="启用状态 （0正常 1停用）", help_text="启用状态 （0正常 1停用）")
    menuCheckStrictly = models.BooleanField(default=True, verbose_name="菜单树选择项是否关联显示", help_text="菜单树选择项是否关联显示")
    deptCheckStrictly = models.BooleanField(default=True, verbose_name="部门树选择项是否关联显示", help_text="部门树选择项是否关联显示")
    delFlag = models.CharField(max_length=4, default="0", verbose_name="是否删除 （0代表存在 2代表删除）", help_text="是否删除 （0代表存在 2代表删除）")

    class Meta:
        db_table = 'system_role'
        verbose_name = '角色管理'
        indexes = [models.Index(fields=['roleId'], name='SystemRole_roleId')]


class SystemUser(CoreModel):
    userId = models.CharField(unique=True, max_length=64, default="", verbose_name="用户id", help_text="用户id")
    deptId = models.CharField(max_length=64, default="", verbose_name="部门id", help_text="部门id")
    username = models.CharField(max_length=64, default="", verbose_name="用户账号", help_text="用户账号")
    nickName = models.CharField(max_length=64, default="", verbose_name="用户昵称", help_text="用户昵称")
    userType = models.CharField(max_length=4, default="00", verbose_name="用户类型（00系统用户）", help_text="用户类型（00系统用户）")
    email = models.CharField(max_length=64, default="", verbose_name="邮箱", help_text="邮箱")
    phone = models.CharField(max_length=64, default="", verbose_name="手机号码", help_text="手机号码")
    avatar = models.CharField(max_length=64, default="", verbose_name="头像", help_text="头像")
    password = models.CharField(max_length=64, default="", verbose_name="密码（加密后）", help_text="密码（加密后）")
    status = models.CharField(max_length=4, default="0", verbose_name="帐号状态（0正常 1停用）", help_text="帐号状态（0正常 1停用）")
    delFlag = models.CharField(max_length=4, default="0", verbose_name="删除标志（0代表存在 2代表删除）", help_text="删除标志（0代表存在 2代表删除）")
    loginIp = models.CharField(max_length=64, default="", verbose_name="最后登陆ip", help_text="最后登陆ip")
    loginDate = models.CharField(max_length=64, default="", verbose_name="最后登陆日期", help_text="最后登陆日期")

    class Meta:
        db_table = 'system_user'
        verbose_name = '用户管理'
        indexes = [models.Index(fields=['userId'], name='SystemUser_userId')]


class SystemRoleMenu(CoreModel):
    menuId = models.CharField(max_length=64, default="", verbose_name="菜单id", help_text="菜单id")
    roleId = models.CharField(max_length=64, default="", verbose_name="角色id", help_text="角色id")

    class Meta:
        db_table = 'system_role_menu'
        verbose_name = '角色与目录关系映射'
        indexes = [models.Index(fields=['roleId'], name='SystemRoleMenu_roleId')]


class SystemUserRole(CoreModel):
    userId = models.CharField(max_length=64, default="", verbose_name="菜单id", help_text="用户id")
    roleId = models.CharField(max_length=64, default="", verbose_name="角色id", help_text="角色id")

    class Meta:
        db_table = 'system_role_user'
        verbose_name = '角色与人员关系映射'
