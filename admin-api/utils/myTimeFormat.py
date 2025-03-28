# -*- coding: utf-8 -*- 
"""
@Author: 孟颖
@email: 652044581@qq.com
@date: 2023/4/23 10:03
@desc: 时间类，生成各类的时间和时间格式转换
"""
import time
from datetime import datetime, timedelta


class MyTimeUtils:
    dateTimeType = '%Y-%m-%d %H:%M:%S'
    dateType = '%Y-%m-%d'
    timeType = '%H:%M:%S'
    fileTimeType = "%Y%m%d%H%M%S%f"
    fileTimeShortType = "%Y%m%d%H%M%S"

    @classmethod
    def TimeFormat(cls, now_time: datetime = datetime.now(), timeType: str = dateTimeType) -> str:
        return now_time.strftime(timeType)

    @classmethod
    def TimeFormatCh(cls, now_time: datetime = datetime.now()) -> str:
        ch_time = now_time.strftime(cls.dateType)
        return "%s年%s月%s日" % tuple(ch_time.split("-"))

    @classmethod
    def TimestampFormat(cls, long: bool = False) -> int:
        return int(time.time() * 1000) if long else int(time.time())

    @classmethod
    def TimeOffsetFormat(cls, start_time: datetime = datetime.now(), days: int = 0, hour: int = 0, minute: int = 0, second: int = 0,
                         timeType: str = dateTimeType) -> str:
        offsetDateTime = start_time + timedelta(days=days, hours=hour, minutes=minute, seconds=second)
        return cls.TimeFormat(offsetDateTime, timeType)


if __name__ == '__main__':
    print(MyTimeUtils.TimeOffsetFormat(days=-1, timeType=MyTimeUtils.fileTimeType))
    print(MyTimeUtils.TimeFormatCh())
