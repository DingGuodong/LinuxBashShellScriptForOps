#!/usr/bin/python
# encoding: utf-8
# -*- coding: utf8 -*-
"""
Created by PyCharm.
File Name:              LinuxBashShellScriptForOps:pyConnectSQLServerWithpyodbcQuickTest.py
Version:                0.0.1
Author:                 Guodong
Author Email:           dgdenterprise@gmail.com
URL:                    https://github.com/DingGuodong/LinuxBashShellScriptForOps
Download URL:           https://github.com/DingGuodong/LinuxBashShellScriptForOps/tarball/master
Create Date:            2018/2/26
Create Time:            19:47
Description:            
Long Description:       
References:             https://docs.microsoft.com/en-us/sql/connect/python/python-driver-for-sql-server
                        https://docs.microsoft.com/en-us/sql/connect/odbc/download-odbc-driver-for-sql-server
                        https://docs.microsoft.com/en-us/sql/connect/python/pyodbc/step-3-proof-of-concept-connecting-to-sql-using-pyodbc
Prerequisites:          pyodbc
Development Status:     3 - Alpha, 5 - Production/Stable
Environment:            Console
Intended Audience:      System Administrators, Developers, End Users/Desktop
License:                Freeware, Freely Distributable
Natural Language:       English, Chinese (Simplified)
Operating System:       POSIX :: Linux, Microsoft :: Windows
Programming Language:   Python :: 3

Topic:                  Utilities
 """
import pyodbc
from collections import Iterable

# https://github.com/mkleehammer/pyodbc/wiki/Connecting-to-SQL-Server-from-Windows
driver = '{ODBC Driver 17 for SQL Server}'
# other not tested driver as follows:
# {SQL Server} - released with SQL Server 2000
# {SQL Native Client} - released with SQL Server 2005 (also known as version 9.0)
# {SQL Server Native Client 10.0} - released with SQL Server 2008
# {SQL Server Native Client 11.0} - released with SQL Server 2012
# {ODBC Driver 11 for SQL Server} - supports SQL Server 2005 through 2014
# {ODBC Driver 13 for SQL Server} - supports SQL Server 2005 through 2016
# {ODBC Driver 17 for SQL Server}
server = 'rdsxxxx.sqlserver.rds.aliyuncs.com'
port = 3433
database = 'database_name'
username = 'username'
password = 'password'

try:
    _ = pyodbc.connect(
        r'DRIVER={driver};SERVER={server},{port};DATABASE={database};UID={username};PWD={password}'.format(
            driver=driver, server=server, port=port, database=database, username=username, password=password),
        timeout=10  # timeout maybe not works
    )
except pyodbc.DatabaseError as e:
    if isinstance(e.args, Iterable):
        for arg in e.args:
            print(arg)
    else:
        print(e.args)
except pyodbc.InterfaceError as e:
    if isinstance(e.args, Iterable):
        for arg in e.args:
            print(arg)
    else:
        print(e.args)
else:
    print("success")
