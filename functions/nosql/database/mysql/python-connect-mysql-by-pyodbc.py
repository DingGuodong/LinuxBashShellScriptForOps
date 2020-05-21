#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created by PyCharm.
File Name:              LinuxBashShellScriptForOps:python-connect-mysql-by-pyodbc.py
Version:                0.0.1
Author:                 dgden
Author Email:           dgdenterprise@gmail.com
URL:                    https://github.com/DingGuodong/LinuxBashShellScriptForOps
Download URL:           https://github.com/DingGuodong/LinuxBashShellScriptForOps/tarball/master
Create Date:            2020/5/21
Create Time:            9:56
Description:            retrieve Chinese Character from MySQL database using pyodbc
Long Description:       **ATTENTION: this is NOT a best choice, due to boring encode and decode**
References:             [Connecting to MySQL](https://github.com/mkleehammer/pyodbc/wiki/Connecting-to-MySQL)
Prerequisites:          download 'Connector/ODBC' for MySQL from https://dev.mysql.com/downloads/connector/odbc/
                        pip install pyodbc
Development Status:     3 - Alpha, 5 - Production/Stable
Environment:            Console
Intended Audience:      System Administrators, Developers, End Users/Desktop
License:                Freeware, Freely Distributable
Natural Language:       English, Chinese (Simplified)
Operating System:       POSIX :: Linux, Microsoft :: Windows
Programming Language:   Python :: 3
Topic:                  Utilities
 """
import locale
import sys

import pyodbc

local_encoding = locale.getpreferredencoding()  # such as 'cp936' or 'gbk' in China


connection_string = (  # type: str
    'DRIVER=MySQL ODBC 8.0 ANSI Driver;'
    'SERVER=localhost;'
    'DATABASE=test;'
    'UID=dev;'
    'PWD=dEvp@ssw0rd;'
    'charset=utf8mb4;'
)

try:
    cnxn = pyodbc.connect(
        connection_string,
        timeout=30
    )
except Exception as e:
    print(e)
    print(", ".join([x for x in e.args]))
    sys.exit(1)

cursor = cnxn.cursor()

cursor.execute(r"""SELECT * FROM test.test""")
row = cursor.fetchone()
while row:
    print("KeyName=%d, ValueName=%s" % (row[0], row[1].encode(local_encoding).decode("utf-8")))
    row = cursor.fetchone()

