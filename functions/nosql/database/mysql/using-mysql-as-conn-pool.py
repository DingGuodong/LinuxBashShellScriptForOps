#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created by PyCharm.
File Name:              LinuxBashShellScriptForOps:using-mysql-as-conn-pool.py
Version:                0.0.1
Author:                 dgden
Author Email:           dgdenterprise@gmail.com
URL:                    https://github.com/DingGuodong/LinuxBashShellScriptForOps
Download URL:           https://github.com/DingGuodong/LinuxBashShellScriptForOps/tarball/master
Create Date:            2020/7/6
Create Time:            10:05
Description:            Python implementation of database connection pool
Long Description:       
References:             
Prerequisites:          pip install mysql-connector-python==8.0.17
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
from mysql.connector import Error
from mysql.connector.cursor import MySQLCursorDict
from mysql.connector.pooling import MySQLConnectionPool

pool = MySQLConnectionPool(pool_name="mypool", pool_size=2, pool_reset_session=True,
                           host='127.0.0.1', database='test', user='dev', password='dEvp@ssw0rd',
                           )


def fetch_one(sql, args=None):
    trans = pool.get_connection()
    obj = None
    try:
        cursor = trans.cursor(cursor_class=MySQLCursorDict)
        cursor.execute(sql, args)
        obj = cursor.fetchall()
        trans.commit()
    except Error as e:
        print(e)
        trans.rollback()
    finally:
        trans.close()

    return obj


def fetch_all(sql, args=None):
    trans = pool.get_connection()
    obj = None
    try:
        cursor = trans.cursor(cursor_class=MySQLCursorDict)
        cursor.execute(sql, args)
        obj = cursor.fetchall()
        trans.commit()
    except Error as e:
        print(e)
        trans.rollback()
    finally:
        trans.close()

    return obj


if __name__ == '__main__':
    print(fetch_all("select * from test.kvt"))
