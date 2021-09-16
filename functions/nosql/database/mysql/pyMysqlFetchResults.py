#!/usr/bin/python
# encoding: utf-8
# -*- coding: utf8 -*-
"""
Created by PyCharm.
File:               LinuxBashShellScriptForOps:pyMysqlFetchResults.py
User:               Guodong
Create Date:        2017/6/5
Create Time:        14:16
 """

import pymysql
import sys
from collections import OrderedDict
from pymysql.cursors import Cursor
from pymysql.cursors import DictCursorMixin


class DictCursorMixinOverride(DictCursorMixin):
    # override this to use OrderedDict or other dict-like types.
    dict_type = OrderedDict


class DictCursor(DictCursorMixinOverride, Cursor):
    """A cursor which returns results as a dictionary"""


sql = "SELECT * FROM `kvt` LIMIT 0, 1000"

connection = pymysql.connect(host='localhost', user='dev', passwd='dEvp@ssw0rd', db='test', port=3306,
                             charset='utf8',
                             cursorclass=DictCursor)

try:
    with connection.cursor() as cursor:
        cursor.execute(sql)
    connection.commit()
finally:
    connection.close()
if cursor is not None:
    results = cursor.fetchall()
    for result in results:
        for k, v in result.items():
            print(k, v)
else:
    print('This will never be reached when join gevent')
    sys.exit(1)
