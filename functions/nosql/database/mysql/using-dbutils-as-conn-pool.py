#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created by PyCharm.
File Name:              LinuxBashShellScriptForOps:using-dbutils-as-conn-pool.py
Version:                0.0.1
Author:                 dgden
Author Email:           dgdenterprise@gmail.com
URL:                    https://github.com/DingGuodong/LinuxBashShellScriptForOps
Download URL:           https://github.com/DingGuodong/LinuxBashShellScriptForOps/tarball/master
Create Date:            2020/7/3
Create Time:            11:01
Description:            Python implementation of database connection pool
Long Description:

[PersistentDB or PooledDB, Which one to use?](https://webwareforpython.github.io/DBUtils/UsersGuide.html)
So which of these two modules should you use? From the above explanations it is clear that
PersistentDB will make more sense if your application keeps a constant number of threads which
frequently use the database. In this case, you will always have the same amount of open database connections.
However, if your application frequently starts and ends threads, then it will be better to use PooledDB.
The latter will also allow more fine-tuning, particularly if you are using a thread-safe DB-API 2 module.

If you are using one of the popular object-relational mappers
[SQLObject](http://www.sqlobject.org/) or [SQLAlchemy](http://www.sqlalchemy.org/),
you won't need DBUtils, since they come with their own connection pools.

References:             
Prerequisites:          pip install DBUtils==1.3
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
import pymysql  # import used DB-API 2 module
from DBUtils.PooledDB import PooledDB

pool = PooledDB(pymysql, mincached=2,
                host="127.0.0.1", database='test', user="dev", password="dEvp@ssw0rd",
                charset='utf8mb4',
                cursorclass=pymysql.cursors.DictCursor)


def fetch_one(sql, args=None):
    trans = pool.connection()
    try:
        with trans.cursor() as cursor:
            cursor.execute(sql, args)  # type:pymysql.cursors
            obj = cursor.fetchone()
        trans.commit()
    except pymysql.Error as e:
        print(e)
        trans.rollback()
    finally:
        trans.close()

    return obj


def fetch_all(sql, args=None):
    trans = pool.connection()
    try:
        with trans.cursor() as cursor:
            cursor.execute(sql, args)  # type:pymysql.cursors
            obj = cursor.fetchall()
        trans.commit()
    except pymysql.Error as e:
        print(e)
        trans.rollback()
    finally:
        trans.close()

    return obj


if __name__ == '__main__':
    print(fetch_all("select * from test.kvt"))
