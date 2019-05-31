#!/usr/bin/python
# encoding: utf-8
# -*- coding: utf8 -*-
"""
Created by PyCharm.
File Name:              LinuxBashShellScriptForOps:pyConnectSQLServerWithpymssqlQuickTest.py
Version:                0.0.1
Author:                 Guodong
Author Email:           dgdenterprise@gmail.com
URL:                    https://github.com/DingGuodong/LinuxBashShellScriptForOps
Download URL:           https://github.com/DingGuodong/LinuxBashShellScriptForOps/tarball/master
Create Date:            2018/2/27
Create Time:            11:10
Description:            
Long Description:       
References:             https://docs.microsoft.com/en-us/sql/connect/python/pymssql/python-sql-driver-pymssql
                        https://docs.microsoft.com/en-us/sql/connect/python/pymssql/step-3-proof-of-concept-connecting-to-sql-using-pymssql
                        https://www.lfd.uci.edu/~gohlke/pythonlibs/#pymssql
Prerequisites:          []
Development Status:     3 - Alpha, 5 - Production/Stable
Environment:            Console
Intended Audience:      System Administrators, Developers, End Users/Desktop
License:                Freeware, Freely Distributable
Natural Language:       English, Chinese (Simplified)
Operating System:       POSIX :: Linux, Microsoft :: Windows
Programming Language:   Python :: 3

Topic:                  Utilities
 """
import pymssql
from collections import Iterable

server = 'rdsxxxx.sqlserver.rds.aliyuncs.com'
port = '3433'
database = 'database_name'
username = 'username'
password = 'password'

try:
    _ = pymssql.connect(server=server, port=port, user=username, password=password, database=database,
                        login_timeout=10)
except pymssql.DatabaseError as e:
    if isinstance(e.args, Iterable):
        for arg in e.args:
            print(arg)
    else:
        print(e.args)
except pymssql.InterfaceError as e:
    if isinstance(e.args, Iterable):
        for arg in e.args:
            print(arg)
    else:
        print(e.args)
else:
    print("success")
