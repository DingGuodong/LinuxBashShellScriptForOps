#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created by PyCharm.
File Name:              LinuxBashShellScriptForOps:insert-data-into-mysql.py
Version:                0.0.1
Author:                 dgden
Author Email:           dgdenterprise@gmail.com
URL:                    https://github.com/DingGuodong/LinuxBashShellScriptForOps
Download URL:           https://github.com/DingGuodong/LinuxBashShellScriptForOps/tarball/master
Create Date:            2020/6/18
Create Time:            10:38
Description:            insert data into mysql
Long Description:       
References:             
Prerequisites:          pip install pymysql
Development Status:     3 - Alpha, 5 - Production/Stable
Environment:            Console
Intended Audience:      System Administrators, Developers, End Users/Desktop
License:                Freeware, Freely Distributable
Natural Language:       English, Chinese (Simplified)
Operating System:       POSIX :: Linux, Microsoft :: Windows
Programming Language:   Python :: 3
Topic:                  Utilities
 """
import pymysql


def save_data_to_mysql(args):
    # If args is a list or tuple, %s can be used as a placeholder in the query.
    # If args is a dict, %(name)s can be used as a placeholder in the query.
    # learn from: cursor.execute()
    # [Python MySQLdb issues (TypeError: %d format: a number is required, not str)]
    # (https://stackoverflow.com/questions/5785154/python-mysqldb-issues-typeerror-d-format-a-number-is-required-not-str)
    # The format string is not really a normal Python format string. You must always use %s for all fields.
    # -> that is: here %s is NOT formatter, but is a placeholder
    sql = 'INSERT INTO `price`(`PSort`, `PName`, `PPrice`, `LPrice`, `MPrice`, `Standard`, `ReleaseTime`) ' \
          'VALUES ( ' \
          '%(PSort)s,' \
          '%(PName)s,' \
          '%(PPrice)s,' \
          '%(LPrice)s,' \
          '%(MPrice)s,' \
          '%(Standard)s,' \
          '%(ReleaseTime)s' \
          ');'

    trans = pymysql.connect(host='127.0.0.1', user='dev', passwd='dEvp@ssw0rd', db='test', port=3306,
                            charset='utf8mb4',
                            cursorclass=pymysql.cursors.DictCursor)

    try:
        with trans.cursor() as cursor:
            cursor.execute(sql, args)
        trans.commit()
    except pymysql.Error as e:
        print(e)
        trans.rollback()
    finally:
        trans.close()
