# -*- coding: utf-8 -*-
"""
@Author ：mengying
@Date   ：2024/12/16 11:39
@Email  : 652044581@qq.com
@Desc   : 功能描述
"""
import pymysql

from config import config


def delete_database():
    """项目启动自动创建数据表"""
    connection = pymysql.connect(host=config.MYSQL_HOST, port=config.MYSQL_PORT, user=config.MYSQL_USER, passwd=config.MYSQL_PASSWORD)
    create_database_sql = f"DROP DATABASE IF EXISTS {config.MYSQL_DB};"
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


# 删除数据库
delete_database()