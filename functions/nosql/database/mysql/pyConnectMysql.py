#!/usr/bin/python
# encoding: utf-8
# -*- coding: utf8 -*-
"""
Created by PyCharm.
File:               LinuxBashShellScriptForOps:pyConntect.py
User:               Guodong
Create Date:        2016/9/13
Create Time:        11:29

# https://stackoverflow.com/questions/26866147/mysql-python-install-error-cannot-open-include-file-config-win-h
# https://www.lfd.uci.edu/~gohlke/pythonlibs/#mysql-python
pip install MySQL-python
pip install https://download.lfd.uci.edu/pythonlibs/t4jqbe6o/MySQL_python-1.2.5-cp27-none-win32.whl

pip install mysql
 """

import sys

import MySQLdb
import datetime

try:
    sql = 'select now()'
    conn = MySQLdb.Connect(host='localhost', user='root', passwd='', db='test', port=3306, charset='utf8')
    cur = conn.cursor()
    start_time = datetime.datetime.now()
    rows = cur.execute(sql)
    result = cur.fetchall()
    end_time = datetime.datetime.now()
    time = (end_time - start_time).microseconds / 1000000.000
    print "%d rows in set (%f sec)" % (rows, time)
    for record in result:
        print record
    cur.close()
    conn.close()
except MySQLdb.Error, e:
    print "Mysql Error %d: %s" % (e.args[0], e.args[1])
    sys.exit(1)
