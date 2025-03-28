# -*- coding: utf-8 -*-
"""
@Author ：mengying
@Date   ：2024/5/31 17:31
@Email  : 652044581@qq.com
@Desc   : 创建数据库
"""
import pymysql

from config import config


def create_database():
    """项目启动自动创建数据表"""
    connection = pymysql.connect(host=config.MYSQL_HOST, port=config.MYSQL_PORT, user=config.MYSQL_USER, passwd=config.MYSQL_PASSWORD)
    create_database_sql = f"CREATE DATABASE IF NOT EXISTS {config.MYSQL_DB} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"
    try:
        # 创建游标对象
        with connection.cursor() as cursor:
            # 执行SQL语句
            cursor.execute(create_database_sql)
        # 提交事务
        connection.commit()
    except pymysql.MySQLError as e:
        print(f"Error: {e}")
    finally:
        # 关闭数据库连接
        connection.close()


# 初始化创建数据库
create_database()
