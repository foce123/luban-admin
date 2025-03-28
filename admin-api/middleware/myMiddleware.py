# -*- coding: utf-8 -*-
"""
@Author ：mengying
@Date   ：2024/5/30 14:16
@Email  : 652044581@qq.com
@Desc   : 功能描述
"""
import logging
import time
import traceback
import uuid

from django.http.response import JsonResponse

from middleware.myAuthorization import Authorization
from utils.myResFormat import ResultJson, ResultCode

logger = logging.getLogger("django")

from django.utils.deprecation import MiddlewareMixin


class AuthMiddleware(MiddlewareMixin):
    """用户认证中间件"""

    def process_request(self, request):
        # 获取用户信息
        Authorization.get_user_info(request)

        # 检查白名单
        if not Authorization.white_list_check(request):
            user_info = getattr(request.headers, 'user_info', {})
            if not user_info:
                return JsonResponse(ResultJson(ResultCode.TOKEN_ERROR).result)

    def process_response(self, request, response):  # 基于请求响应
        return response

    def process_exception(self, request, exception):

        formatter = ["接口地址 :   %s" % request.get_full_path(), "请求方式 :   %s" % request.method, "请求参数 :   body: %s" % request.body.decode(),
                     "用户信息 :   user: %s" % str(getattr(request.headers, 'user_info', {})), "报错信息 :   %s" % str(traceback.format_exc())]
        error_message = "\n".join(formatter)
        logger.error(error_message)
        return JsonResponse(ResultJson(ResultCode.SERVER_ERROR, description=str(exception)).result)


class LogMiddleware(MiddlewareMixin):
    """记录日志中间件"""

    def process_request(self, request):
        uid = uuid.uuid4().hex
        setattr(request.headers, "my-duration", time.time())
        setattr(request.headers, "uid", uid)
        self.recordsRequest(uid, request.get_full_path(), request.method, request.body.decode())

    def process_response(self, request, response):  # 基于请求响应
        duration = time.time() - getattr(request.headers, "my-duration")
        uid = getattr(request.headers, "uid")
        self.recordsResponse(uid, request.get_full_path(), response.content.decode(), duration)
        return response

    @classmethod
    def white_path(cls, path):
        request_white_path = []
        return path in request_white_path

    @classmethod
    def recordsRequest(cls, uid, path, method, data):
        request_info = '链路id: %s  接口: %s  请求方式: %s  body参数: %s' % (uid, path, method, data)
        if cls.white_path(path):
            return
        logger.info(str(request_info))

    @classmethod
    def recordsResponse(cls, uid, path, data, duration=None):
        response_info = '链路id: %s  接口: %s  返回数据: %s  耗时: %s ' % (uid, path, data, duration)
        if cls.white_path(path):
            return
        logger.info(str(response_info))
