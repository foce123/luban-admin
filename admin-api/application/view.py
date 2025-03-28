# -*- coding: utf-8 -*-
"""
@Author ：mengying
@Date   ：2024/6/13 14:27
@Email  : 652044581@qq.com
@Desc   : 分页器
"""

import json

from pydantic import ValidationError
from rest_framework.views import APIView


class APIViewReBuilder(APIView):
    requestBody = None
    requestParams = None
    requestPath = None

    def dispatch(self, request, *args, **kwargs):
        annotations = self.__class__.__annotations__
        bodyType = annotations.get("requestBody")
        paramsType = annotations.get("requestParams")

        if bodyType:
            requestBody = self.checkType(bodyType, request.body.decode())
            request.META["requestBody"] = requestBody

        if paramsType:
            requestParams = self.checkType(bodyType, request.GET)
            kwargs = {requestParams: requestParams, **kwargs}

        return super().dispatch(request, *args, **kwargs)

    @classmethod
    def checkType(cls, model, data):
        try:
            if isinstance(data, str):
                data = json.loads(data)
            return model.model_validate(data).model_dump_json()
        except ValidationError as e:
            raise Exception("参数校验失败")
