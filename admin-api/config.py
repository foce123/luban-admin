# -*- coding: utf-8 -*-
"""
@Author：mengying
@file： config.py
@date：2023/12/18 9:35
@email: 652044581@qq.com
@desc: 
"""
import nacos
from addict import Dict
import json


class Localconfig:
    """本地配置（二选一）"""

    # 项目的名称
    PROJECT_NAME = "luban-admin"

    # 配置redis缓存地址
    REDIS_HOST = '127.0.0.1'
    REDIS_PORT = 6379
    REDIS_DB = 0
    REDIS_PASSWORD = "123456"

    # 配置mongo数据库
    MYSQL_DB = "lbdj_admin"  # 注： 数据库名不能用-特殊字符
    MYSQL_HOST = "127.0.0.1"
    MYSQL_PORT = 3306
    MYSQL_USER = "root"
    MYSQL_PASSWORD = "luban123456"
    MYSQL_ENGINE = 'django.db.backends.mysql'

    # 加密随机串(hash-md5)
    ENCRYPT_STRING = "c-QULBDJ-+u=-BUSQ$"

    DEBUG = True

    @classmethod
    def get_server_config(cls):
        return {item: getattr(cls, item) for item in dir(cls)}


class NacosClient:
    """nacos配置（二选一）"""

    def __init__(self, addr: str = None, namespace: str = None, data_id: str = None, group_id: str = None,
                 username: str = "nacos", password: str = "nacos"):
        self.addr = addr or "120.46.187.114:8848"
        self.namespace = namespace or "7d35aedc-ec57-48c8-8489-9974d19a2942"
        self.data_id = data_id or "sigin"
        self.group_id = group_id or "dev"
        self.client = nacos.NacosClient(self.addr, namespace=self.namespace, username=username, password=password)

    def get_server_config(self):
        print(self.client.get_config(self.data_id, self.group_id))
        return json.loads(self.client.get_config(self.data_id, self.group_id))


# nacos的配置
# config = Dict(NacosClient().get_server_config())

# 本地的配置
config = Dict(Localconfig.get_server_config())

if __name__ == '__main__':
    print(config.MYSQL_DB)
