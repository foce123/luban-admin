# -*- coding: utf-8 -*- 
"""
========================================================================================================================
@file: myResFormat
@Author: mengying
@email: 652044581@qq.com
@date: 2023/3/3 12:14
@desc: 返回的数据格式定义
========================================================================================================================
"""
from addict import Dict


class ResultCode:
    """
    @param: code返回码
    @param: msg信息
    @param: description描述
    @desc: 返回码
    """
    SUCCESS = (200, '操作成功', None)
    FAIL = (500, '操作失败', None)
    TOKEN_ERROR = (401, 'token过期', None)
    SERVER_ERROR = (500, '服务错误', None)
    DEPT_ERROR = (500, '部门名称重复', None)
    ROLE_ERROR = (500, '角色名称或权限字符重复', None)
    USER_ERROR = (500, '用户名已存在', None)
    MENU_ERROR = (500, '目录名称重复', None)
    PASSWORD_ERROR = (500, '密码错误', None)
    AUTH_CODE_EXP = (500, '验证码过期', None)
    AUTH_CODE_ERROR = (500, '验证码错误', None)
    PRE_AUTH_ERROR = (400, '权限不足', None)
    USER_NOT_EXIST = (500, '用户不存在', None)
    USER_NOT_ALLOW = (500, '用户被禁用，请联系系统管理员', None)
    DEMO_ERROR = (500, 'demo模式不允许修改', None)


class ResultJson:
    result = Dict()

    def __init__(self, ret=ResultCode.SUCCESS, data=None, description=None, postscript=None):
        self.result.code = ret[0]
        self.result.msg = ret[1] % postscript if postscript else ret[1]
        self.result.data = data
        self.result.description = description or ret[2]


if __name__ == '__main__':
    print(ResultJson(ret=ResultCode.SUCCESS, data=None, description="成功").result)
