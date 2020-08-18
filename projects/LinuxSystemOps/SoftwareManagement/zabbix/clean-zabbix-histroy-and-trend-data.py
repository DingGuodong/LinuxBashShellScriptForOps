#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created by PyCharm.
File Name:              LinuxBashShellScriptForOps:clean-zabbix-histroy-and-trend-data.py
Version:                0.0.1
Author:                 dgden
Author Email:           dgdenterprise@gmail.com
URL:                    https://github.com/DingGuodong/LinuxBashShellScriptForOps
Download URL:           https://github.com/DingGuodong/LinuxBashShellScriptForOps/tarball/master
Create Date:            2020/8/18
Create Time:            9:55
Description:            clean zabbix history and trend data for small zabbix instance
Long Description:       
References:             [Zabbix数据库表分区](https://www.cnblogs.com/w787815/p/8249303.html)
Prerequisites:          []
Development Status:     3 - Alpha, 5 - Production/Stable
Environment:            Console
Intended Audience:      System Administrators, Developers, End Users/Desktop
License:                Freeware, Freely Distributable
Natural Language:       English, Chinese (Simplified)
Operating System:       POSIX :: Linux, Microsoft :: Windows
Programming Language:   Python :: 2.6
Programming Language:   Python :: 2.7
Topic:                  Utilities
 """

from mysql.connector import Error
from mysql.connector.cursor import MySQLCursorDict
from mysql.connector.pooling import MySQLConnectionPool

pool = MySQLConnectionPool(pool_name="mypool", pool_size=2, pool_reset_session=False,
                           host='120.27.192.32', port='3306', database='zabbix', user='dev', password='s4kt6GUeqb7V_ZV',
                           )


def timeit(func):
    """
    测量函数执行所用时间的装饰器
    https://stackoverflow.com/questions/8885663/how-to-format-a-floating-number-to-fixed-width-in-python
    :param func:
    :return:
    """
    from functools import wraps

    @wraps(func)
    def func_timer(*args, **kwargs):
        import time
        time_begin = time.time()
        result = None
        try:
            result = func(*args, **kwargs)
        except Exception as e:
            print(e)
        time_end = time.time()
        msg = "- - INFO: Total time running {func_name}: {time_spent:16.8f} seconds".format(func_name=func.__name__,
                                                                                            time_spent=time_end - time_begin)
        print(msg)
        return result

    return func_timer


@timeit
def fetch_one(sql, args=None):
    trans = pool.get_connection()
    obj = None
    try:
        cursor = trans.cursor(cursor_class=MySQLCursorDict)
        cursor.execute(sql, args)
        obj = cursor.fetchone()
        trans.commit()
    except Error as e:
        print(e)
        trans.rollback()
    finally:
        trans.close()

    return obj


if __name__ == '__main__':
    print(fetch_one("SELECT now() AS now"))

    sql_to_get_counts_from_zbx = '''
    SELECT count('clock') AS history_uint_count FROM history_uint WHERE clock < UNIX_TIMESTAMP(DATE_SUB(NOW(), INTERVAL 14 DAY));
SELECT count('clock') AS history_count FROM history WHERE clock < UNIX_TIMESTAMP(DATE_SUB(NOW(), INTERVAL 14 DAY));
SELECT count('clock') AS trends_uint_count FROM trends_uint WHERE clock < UNIX_TIMESTAMP(DATE_SUB(NOW(), INTERVAL 14 DAY));
SELECT count('clock') AS trends_count FROM trends WHERE clock < UNIX_TIMESTAMP(DATE_SUB(NOW(), INTERVAL 14 DAY));
SELECT count('clock') AS events_count FROM events WHERE clock < UNIX_TIMESTAMP(DATE_SUB(NOW(), INTERVAL 14 DAY));
SELECT count('clock') AS alerts_count FROM alerts WHERE clock < UNIX_TIMESTAMP(DATE_SUB(NOW(), INTERVAL 14 DAY));
'''
    for line in sql_to_get_counts_from_zbx.strip().split("\n"):
        print(fetch_one(line.strip()))

    print("- - Hint: you can set index for big table in zabbix database")

    sql_to_delete_old_data_from_zbx = '''
DELETE FROM history_uint WHERE clock < UNIX_TIMESTAMP(DATE_SUB(NOW(), INTERVAL 14 DAY));
DELETE FROM history WHERE clock < UNIX_TIMESTAMP(DATE_SUB(NOW(), INTERVAL 14 DAY));
DELETE FROM trends_uint WHERE clock < UNIX_TIMESTAMP(DATE_SUB(NOW(), INTERVAL 14 DAY));
DELETE FROM trends WHERE clock < UNIX_TIMESTAMP(DATE_SUB(NOW(), INTERVAL 14 DAY));
DELETE FROM events WHERE clock < UNIX_TIMESTAMP(DATE_SUB(NOW(), INTERVAL 14 DAY));
DELETE FROM alerts WHERE clock < UNIX_TIMESTAMP(DATE_SUB(NOW(), INTERVAL 14 DAY));
    '''

    print("- - Hint: NOT recommend for big table in zabbix database, we can use mysql table partition")

    for line in sql_to_delete_old_data_from_zbx.strip().split("\n"):
        print(fetch_one(line.strip()))
