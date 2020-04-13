#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created by PyCharm.
File Name:              LinuxBashShellScriptForOps:get-charset-and-collation.py
Version:                0.0.1
Author:                 dgden
Author Email:           dgdenterprise@gmail.com
URL:                    https://github.com/DingGuodong/LinuxBashShellScriptForOps
Download URL:           https://github.com/DingGuodong/LinuxBashShellScriptForOps/tarball/master
Create Date:            2020/4/13
Create Time:            14:28
Description:            get charset and collation of databases in the db instance
Long Description:       
References:             [再见乱码：5分钟读懂MySQL字符集设置](https://www.cnblogs.com/chyingp/p/mysql-character-set-collation.html)
Prerequisites:          pip install pymysql
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
import sys

import pymysql


def mysql_query(conn, sql):
    """
    mysql query sql on mysql server
    :param conn: 'pymysql.connections.Connection'
    :param sql:  SQL str
    :return:  list
    """
    connection = conn  # type: pymysql.connections.Connection

    with connection.cursor() as cursor:
        cursor.execute(sql)
    connection.commit()

    if cursor is not None:
        return cursor.fetchall()  # type: list
    else:
        return None


if __name__ == '__main__':
    excluded_databases = ['information_schema', 'mysql', 'performance_schema', 'sys']

    try:
        cnx = pymysql.connect(host='localhost', user='dev', passwd='dEvp@ssw0rd', db='test', port=3306,
                              charset='utf8',
                              read_timeout=10, write_timeout=10,
                              cursorclass=pymysql.cursors.DictCursor)
    except pymysql.err.OperationalError as e:
        print(e)
        sys.exit(1)

    # method 1
    sql_result = mysql_query(cnx, "show databases")
    assert sql_result is not None
    databases_list = [result.get("Database") for result in sql_result]

    for database in databases_list:
        if database not in excluded_databases:
            sql_result = mysql_query(cnx, "show create database {db}".format(db=database))
            assert sql_result is not None
            print(sql_result[0].get("Create Database"))

    sql_result = mysql_query(cnx,
                             "select SCHEMA_NAME,DEFAULT_CHARACTER_SET_NAME,DEFAULT_COLLATION_NAME "
                             "FROM information_schema.SCHEMATA")
    # method 2 (preferred)
    for record in sql_result:
        db = record.get('SCHEMA_NAME')
        charset = record.get('DEFAULT_CHARACTER_SET_NAME')
        collation = record.get('DEFAULT_COLLATION_NAME')
        if db not in excluded_databases:
            print("CREATE DATABASE `{db}` CHARACTER SET '{charset}' COLLATE '{collation}';".format(
                db=db, charset=charset, collation=collation
            ))
