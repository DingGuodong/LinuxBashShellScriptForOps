#!/usr/bin/python
# encoding: utf-8
# -*- coding: utf8 -*-
"""
Created by PyCharm.
File:               LinuxBashShellScriptForOps:pyUpdateMysql.py
User:               Guodong
Create Date:        2016/9/28
Create Time:        14:35

pip install mysql
pip install MySQL-python

 """
import MySQLdb
import datetime

password = raw_input("Please input MySQL password:\n")

if password != "":
    pass
else:
    raise RuntimeError

try:
    conn = MySQLdb.Connect(host='localhost', user='root', passwd=password, db='test', port=3306, charset='utf8')
    cur = conn.cursor()
    start_time = datetime.datetime.now()
    rows = cur.execute(' update kvt set key2 = "1" where key1 = "1"')  # print conn.affected_rows()
    result = cur.fetchall()
    end_time = datetime.datetime.now()
    time = (end_time - start_time).microseconds / 1000000.000
    print "%d rows in set (%f sec)" % (rows, time)
    print conn.info()
    for record in result:
        print record
    cur.close()
    conn.close()
except MySQLdb.Error, e:
    print "Mysql Error %d: %s" % (e.args[0], e.args[1])
