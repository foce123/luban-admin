# -*- coding: utf-8 -*-
"""
========================================================================================================================
@Author: 孟颖
@email: 652044581@qq.com
@date: 2023/4/20 10:19
@desc: 枚举模块自定义dict转换
========================================================================================================================
"""
from enum import Enum, unique


class EnumDict(Enum):

    @classmethod
    def transform(cls):
        res = dict()
        for key, value in cls.__members__.items():
            res[key] = value.value
        return res

    @classmethod
    def reverse_transform(cls):
        res = dict()
        for key, value in cls.__members__.items():
            res[value.value] = key
        return res

    @classmethod
    def format_front(cls):
        return [{"label": key, "value": value.value} for key, value in cls.__members__.items()]

    @classmethod
    def get_value(cls, key):
        enum_map = cls.transform()
        return enum_map.get(key)


@unique
class SystemStatusEnum(EnumDict):
    p0 = "0"  # 0正常
    p1 = "1"  # 1停用


@unique
class SystemDelEnum(EnumDict):
    p0 = "0"  # 0存在
    p1 = "2"  # 2删除


@unique
class SystemUserTypeEnum(EnumDict):
    p0 = "00"  # 系统账号
    p1 = "01"  # 管理员账号

