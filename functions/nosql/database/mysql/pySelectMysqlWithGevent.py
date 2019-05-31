#!/usr/bin/python
# encoding: utf-8
# -*- coding: utf8 -*-
"""
Created by PyCharm.
File:               LinuxBashShellScriptForOps:pySelectMysql.py
User:               Guodong
Create Date:        2016/12/1
Create Time:        15:29

Pure Python MySQL Driver, non-blocking
pip install PyMySQL

 """
from gevent import monkey

monkey.patch_all()  # socket module is patched
import gevent
import sys


def mysql_query(sql):
    import pymysql
    connection = pymysql.connect(host='localhost', user='dev', passwd='dEvp@ssw0rd', db='test', port=3306,
                                 charset='utf8',
                                 cursorclass=pymysql.cursors.DictCursor)

    try:
        with connection.cursor() as cursor:
            cursor.execute(sql)
        connection.commit()
    finally:
        connection.close()
    if cursor is not None:
        return cursor
    else:
        print('This will never be reached when joined gevent')
        sys.exit(1)


sql1 = "SELECT * FROM `kvt` LIMIT 0, 1000"
sql2 = "SELECT * FROM `test` LIMIT 0, 1000"
jobs = [gevent.spawn(mysql_query, sql1), gevent.spawn(mysql_query, sql2)]
gevent.joinall(jobs, timeout=2)
result = [job.value for job in jobs]
if result is not None:
    for item in result:
        if item is not None:
            for value in item:
                print(value)
        else:
            print("result:", None)
