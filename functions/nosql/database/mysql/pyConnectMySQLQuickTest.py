#!/usr/bin/python
# encoding: utf-8
# -*- coding: utf8 -*-
"""
Created by PyCharm.
File Name:              LinuxBashShellScriptForOps:pyConnectMySQLQuickTest.py
Version:                0.0.1
Author:                 Guodong
Author Email:           dgdenterprise@gmail.com
URL:                    https://github.com/DingGuodong/LinuxBashShellScriptForOps
Download URL:           https://github.com/DingGuodong/LinuxBashShellScriptForOps/tarball/master
Create Date:            2018/2/27
Create Time:            14:45
Description:            quick test to connect to MySQL Server
Long Description:       
References:             
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
from collections import Iterable

import pymysql

server = 'localhost'
port = 3306
database = 'test'
username = 'dev'
password = 'dEvp@ssw0rd'

try:
    connection = pymysql.connect(host=server, user=username, passwd=password, db=database, port=port,
                                 connect_timeout=10,
                                 charset='utf8',
                                 cursorclass=pymysql.cursors.DictCursor)
except pymysql.Error as e:
    if isinstance(e.args, Iterable):
        for arg in e.args:
            print(arg)
    else:
        print(e.args)
else:
    print("success")
