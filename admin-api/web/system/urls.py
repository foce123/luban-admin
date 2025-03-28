from django.urls import path, re_path

from web.system import views as systemView

urlpatterns = [

    # 部门相关
    path('dept/list', systemView.DeptListView.as_view(), name="部门列表"),
    path('dept', systemView.DeptCreateView.as_view(), name="部门新增/修改"),
    re_path('dept/(?P<deptId>[0-9]+$)', systemView.DeptDetailView.as_view(), name="部门详情/删除"),
    re_path('dept/list/exclude/(?P<deptId>[0-9]+$)', systemView.DeptExcludeView.as_view(), name="部门排除查询"),

    # 角色相关
    path('role/list', systemView.RoleListView.as_view(), name="角色列表"),
    path('role', systemView.RoleCreateView.as_view(), name="角色新增"),
    path('role/changeStatus', systemView.RoleStatusView.as_view(), name="角色状态修改"),
    re_path('role/(?P<roleId>[0-9]+$)', systemView.RoleDetailView.as_view(), name="角色新增"),

    # 角色认证
    path('role/authUser/allocatedList', systemView.AuthUserAllocatedListView.as_view(), name="分配用户列表"),
    path('role/authUser/cancel', systemView.AuthUserCancelView.as_view(), name="角色取消人员授权"),
    path('role/authUser/cancelAll', systemView.AuthUserCancelAllView.as_view(), name="批量取消授权"),
    path('role/authUser/unallocatedList', systemView.AuthUserUnallocatedListView.as_view(), name="未授权用户列表"),
    path('role/authUser/selectAll', systemView.AuthUserSelectAllView.as_view(), name="批量绑定角色人员"),

    # 用户相关
    re_path('user/authRole/(?P<userId>[0-9]+$)', systemView.AuthRoleView.as_view(), name="用户角色绑定"),
    path('user/authRole', systemView.AuthRoleView.as_view(), name="用户角色绑定修改"),
    path('user/list', systemView.UserListView.as_view(), name="用户列表"),
    path('user/deptTree', systemView.UserDeptTreeView.as_view(), name="用户列表"),
    path('user/changeStatus', systemView.UserStatusView.as_view(), name="用户状态修改"),
    path('user/', systemView.UserCreateView.as_view(), name="用户新增"),
    re_path('user/(?P<userId>[0-9 ,]+$)', systemView.UserDetailView.as_view(), name="用户详情/删除"),
    path('user/resetPwd', systemView.UserResetPwdView.as_view(), name="重置密码"),

    # 个人中心
    path('user/profile/updatePwd', systemView.UserUpdatePwdView.as_view(), name="修改密码"),
    path('user/profile', systemView.UserProfileView.as_view(), name="个人中心"),
    path('user/profile/avatar', systemView.UserProfileAvatarView.as_view(), name="修改头像"),

    # 目录相关
    path('menu/list', systemView.MenuListView.as_view(), name="目录列表"),
    re_path('menu/(?P<menuId>[0-9]+$)', systemView.MenuDetailView.as_view(), name="目录详情/删除"),
    path('menu', systemView.MenuCreateView.as_view(), name="目录新增"),
    path('menu/treeselect', systemView.MenuTreeSelectView.as_view(), name="树选择器"),
    re_path('menu/roleMenuTreeselect/(?P<roleId>[0-9]+$)', systemView.MenuRoleTreeSelectView.as_view(), name="已选择的树选择器"),

]
