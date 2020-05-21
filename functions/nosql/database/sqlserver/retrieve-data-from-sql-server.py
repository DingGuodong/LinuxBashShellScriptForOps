#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created by PyCharm.
File Name:              LinuxBashShellScriptForOps:retrieve-data-from-sql-server.py
Version:                0.0.1
Author:                 dgden
Author Email:           dgdenterprise@gmail.com
URL:                    https://github.com/DingGuodong/LinuxBashShellScriptForOps
Download URL:           https://github.com/DingGuodong/LinuxBashShellScriptForOps/tarball/master
Create Date:            2020/5/20
Create Time:            14:51
Description:            retrieve(SELECT) data from Microsoft SQL Server
Long Description:
                        retrieve data using pyodbc is better than pymssql
                            1. easier to install
                            2. needn't require encode and decode to avoid getting unreadable string
References:             
Prerequisites:          pip3.8 isntall pyodbc

                        #pip3.8 install Cython
                        #pip3.8 install pymssql  # https://support.microsoft.com/en-us/help/2977003/the-latest-supported-visual-c-downloads
                        pip3.8 install https://download.lfd.uci.edu/pythonlibs/s2jqpv5t/pymssql-2.1.4-cp38-cp38-win_amd64.whl

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
from collections import Iterable

import pymssql
import pyodbc

server = '192.168.88.33'
port = '1433'
database = 'user'
username = 'sa'
password = r'password'
charset = 'utf8'
local_encoding = locale.getpreferredencoding()  # such as 'cp936' or 'gbk' in China


def retrieve_data_by_pymssql():
    try:
        cnx = pymssql.connect(server=server, port=port, user=username, password=password, database=database,
                              login_timeout=10, charset=charset)
    except pymssql.DatabaseError as e:
        if isinstance(e.message, Iterable):
            print(e)
            print(", ".join([str(x) for x in e.message]))
        else:
            print(e)
        sys.exit(1)
    except pymssql.InterfaceError as e:
        if isinstance(e.message, Iterable):
            print(e)
            print(", ".join([str(x) for x in e.message]))
        else:
            print(e)
        sys.exit(1)
    else:
        print("connected successful")

    cursor = cnx.cursor()
    cursor.execute(r"""SELECT [DepartmentID], [DepartmentName] FROM [dbo].[Department]""")
    row = cursor.fetchone()
    while row:
        # Notes: 'gbk' is equal to 'cp936'; 'latin-1' is equal to 'ISO-8859-1'
        # Notes: 'latin-1', 'latin1' (also known as 'ISO-8859-1') or 'cp1252'(also known as 'Windows-1252')
        # maybe default encoding of MS SQL Server
        # str.encode('latin-1').decode('gbk') to resolve unreadable string
        print("DepartmentID=%d, DepartmentName=%s" % (row[0], row[1].encode('latin1').decode(local_encoding)))
        row = cursor.fetchone()


def retrieve_data_by_pyodbc():
    # https://github.com/mkleehammer/pyodbc/wiki/Connecting-to-SQL-Server-from-Windows
    driver = '{ODBC Driver 17 for SQL Server}'  # {ODBC Driver 17 for SQL Server} - supports SQL Server 2008 through 2019
    try:
        cnx = pyodbc.connect(
            r'DRIVER={driver};SERVER={server};PORT={port};DATABASE={database};UID={username};PWD={password}'.format(
                driver=driver, server=server, port=port, database=database, username=username, password=password),
            timeout=30
        )
    except Exception as e:
        print(e)
        print(", ".join([x for x in e.args]))  # type: unicode
        sys.exit(1)

    cursor = cnx.cursor()
    cursor.execute(r"""SELECT [DepartmentID], [DepartmentName] FROM [dbo].[Department]""")
    row = cursor.fetchone()
    while row:
        print("DepartmentID=%d, DepartmentName=%s" % (row[0], row[1]))
        row = cursor.fetchone()


if __name__ == '__main__':
    retrieve_data_by_pyodbc()
