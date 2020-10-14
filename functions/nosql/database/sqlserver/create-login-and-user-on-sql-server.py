#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created by PyCharm.
File Name:              LinuxBashShellScriptForOps:create-login-and-user-on-sql-server.py
Version:                0.0.1
Author:                 dgden
Author Email:           dgdenterprise@gmail.com
URL:                    https://github.com/DingGuodong/LinuxBashShellScriptForOps
Download URL:           https://github.com/DingGuodong/LinuxBashShellScriptForOps/tarball/master
Create Date:            2020/10/13
Create Time:            17:08
Description:            create login and user for SQL Server
Long Description:       
References:             
Prerequisites:          pip install pyodbc
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
import pyodbc

sql_server = 'localhost'
sql_port = '1433'
sql_username = 'guodong'  # do NOT use 'sa' account in any case
sql_password = 'password'
sql_charset = 'utf8'
sql_database = 'master'

biz_database = 'utestdb'
biz_username = 'utestdbl01'
biz_password = 'utestdbl01'

base_sql = '''
-- 创建登录名
USE [master];
CREATE LOGIN  [{username}] WITH PASSWORD=N'{password}', DEFAULT_DATABASE=[master], CHECK_EXPIRATION=OFF, CHECK_POLICY=OFF;

-- 创建数据库用户
USE [{database_name}];
CREATE USER [{username}] FOR LOGIN [{username}];

-- 授予数据库角色
USE [{database_name}];
ALTER ROLE [db_owner] ADD MEMBER [{username}];
'''

# https://github.com/mkleehammer/pyodbc/wiki/Connecting-to-SQL-Server-from-Windows
sql_driver = '{ODBC Driver 17 for SQL Server}'
cnxn = pyodbc.connect(
    r'DRIVER={driver};SERVER={server};PORT={port}, DATABASE={database};UID={username};PWD={password}'.format(
        driver=sql_driver, server=sql_server, port=sql_port, database=sql_database, username=sql_username,
        password=sql_password),
    timeout=30
)
cursor = cnxn.cursor()
res = cursor.execute('select @@VERSION')
print(res.fetchone()[0])
# TODO(DingGuodong) add logging

# security validation
if biz_database == 'master':
    print("Do NOT use 'master' database for this script")
    exit(1)

# assemble sql statements
biz_sql = base_sql.format(
    username=biz_username,
    password=biz_password,
    database_name=biz_database
)

# show current sql statements
print(biz_sql)

# execute sql statements and commit.
cursor.execute(biz_sql)
cursor.commit()
cursor.close()
