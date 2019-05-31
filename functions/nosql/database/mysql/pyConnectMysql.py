#!/usr/bin/python
# encoding: utf-8
# -*- coding: utf8 -*-
"""
Created by PyCharm.
File:               LinuxBashShellScriptForOps:pyConntect.py
User:               Guodong
Create Date:        2016/9/13
Create Time:        11:29

pip install MySQL-python

 """

import MySQLdb
import datetime
import sys

try:
    sql = 'select now()'
    conn = MySQLdb.Connect(host='localhost', user='root', passwd='', db='test', port=3306, charset='utf8')
    cur = conn.cursor()
    start_time = datetime.datetime.now()
    rows = cur.execute(sql)
    result = cur.fetchall()
    end_time = datetime.datetime.now()
    time = (end_time - start_time).microseconds / 1000000.000
    print("%d rows in set (%f sec)" % (rows, time))
    for record in result:
        print(record)
    cur.close()
    conn.close()
except MySQLdb.Error as e:
    print("Mysql Error %d: %s" % (e.args[0], e.args[1]))
    sys.exit(1)
