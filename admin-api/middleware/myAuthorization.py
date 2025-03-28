# -*- coding: <encoding name> -*-
"""
@Author：mengying
@file： myAuthorization.py
@date：2023/6/14 16:46
@email: 652044581@qq.com
@desc: 授权相关
"""
import json

from django_redis import get_redis_connection


class CacheKeys:
    TOKEN_NAME = "Authorization"


class Authorization:

    @staticmethod
    def get_user_info(request):
        """从header中获取访问人员信息放在header中"""
        RedisClient = get_redis_connection()

        token = request.headers.get(CacheKeys.TOKEN_NAME, '')

        if not token:
            setattr(request.headers, "user_info", {})
            return None

        user = RedisClient.get(token)
        RedisClient.expire(token, 30 * 60)

        if user:
            user = json.loads(user)
            user["token"] = token
        else:
            user = {}

        setattr(request.headers, "user_info", user)

    @staticmethod
    def white_list_check(request):
        """判断访问名路径是否是白名单"""

        white_list = ['/api/login', '/api/captchaImage', '/api/logout']
        if request.path in white_list:
            return True
        else:
            return False
