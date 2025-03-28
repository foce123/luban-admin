# -*- coding: utf-8 -*- 
"""
========================================================================================================================
@project : my-sanic
@file: myUUID
@Author: mengying
@email: 652044581@qq.com
@date: 2023/4/4 12:14
@desc: 雪花算法生成分布式id，用户订单生成相关或者uuid使用
========================================================================================================================
"""

import time
from threading import Lock

# 64 位 id 的划分,通常机器位和数据位各为 5 位
WORKER_ID_BITS = 5  # 机器位
DATACENTER_ID_BITS = 5  # 数据位
SEQUENCE_BITS = 12  # 循环位

# 最大取值计算,计算机中负数表示为他的补码
MAX_WORKER_ID = -1 ^ (-1 << WORKER_ID_BITS)  # 2**5 -1 =31
MAX_DATACENTER_ID = -1 ^ (-1 << DATACENTER_ID_BITS)

# 移位偏移计算
WORKER_ID_SHIFT = SEQUENCE_BITS
DATACENTER_ID_SHIFT = SEQUENCE_BITS + WORKER_ID_BITS
TIMESTAMP_LEFT_SHIFT = SEQUENCE_BITS + WORKER_ID_BITS + DATACENTER_ID_BITS

# X序号循环掩码
SEQUENCE_MASK = -1 ^ (-1 << SEQUENCE_BITS)

# Twitter 元年时间戳
TWEPOCH = 1288834974657


class SingletonMeta(type):
    """元类单例"""
    __instance = None
    __lock = Lock()

    def __call__(cls, *args, **kwargs):
        with cls.__lock:
            new = kwargs.pop('new', None)
            if new is True:
                return super().__call__(*args, **kwargs)
            if not cls.__instance:
                cls.__instance = super().__call__(*args, **kwargs)
        return cls.__instance


class SnowIdWorker(metaclass=SingletonMeta):
    """不能实例多次，会生产一样的id"""

    def __init__(self, datacenter_id=1, worker_id=2, sequence=0):
        """
        初始化方法
        :param datacenter_id:数据id
        :param worker_id:机器id
        :param sequence:序列码
        """
        if worker_id > MAX_WORKER_ID or worker_id < 0:
            raise ValueError('worker_id 值越界')
        if datacenter_id > MAX_DATACENTER_ID or datacenter_id < 0:
            raise ValueError('datacenter_id 值越界')

        self.worker_id = worker_id
        self.datacenter_id = datacenter_id
        self.sequence = sequence

        self.last_timestamp = -1  # 上次计算的时间戳

    def _gen_timestamp(self):
        """
        生成整数时间戳。
        :return:
        """
        return int(time.time() * 1000)

    def generate(self) -> str:
        """
        获取新的ID.
        :return:
        """
        # 获取当前时间戳
        timestamp = self._gen_timestamp()

        # 时钟回拨的情况
        if timestamp < self.last_timestamp:
            raise Exception("clock is moving backwards")

        if timestamp == self.last_timestamp:
            # 同一毫秒的处理。
            self.sequence = (self.sequence + 1) & SEQUENCE_MASK
            if self.sequence == 0:
                timestamp = self._til_next_millis(self.last_timestamp)
        else:
            self.sequence = 0

        self.last_timestamp = timestamp

        new_id = (((timestamp - TWEPOCH) << TIMESTAMP_LEFT_SHIFT) | (self.datacenter_id << DATACENTER_ID_SHIFT) | (
                self.worker_id << WORKER_ID_SHIFT)) | self.sequence
        return str(new_id)

    def _til_next_millis(self, last_timestamp):
        """
        等到下一毫秒。
        :param last_timestamp:
        :return:
        """
        timestamp = self._gen_timestamp()
        while timestamp <= last_timestamp:
            timestamp = self._gen_timestamp()
        return timestamp


Sf = SnowIdWorker()

if __name__ == '__main__':
    for i in range(1000):
        print(Sf.generate())
