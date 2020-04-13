#!/usr/bin/python
# encoding: utf-8
# -*- coding: utf8 -*-
"""
Created by PyCharm.
File Name:              LinuxBashShellScriptForOps:pyMysqlFetchResults_u2.py
Version:                0.0.1
Author:                 Guodong
Author Email:           dgdenterprise@gmail.com
URL:                    https://github.com/DingGuodong/LinuxBashShellScriptForOps
Download URL:           https://github.com/DingGuodong/LinuxBashShellScriptForOps/tarball/master
Create Date:            2017/10/17
Create Time:            15:46
Description:            
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
import sys

import prettytable
import pymysql

try:
    connection = pymysql.connect(host='localhost', user='dev', passwd='dEvp@ssw0rd', db='test', port=3306,
                                 charset='utf8',
                                 cursorclass=pymysql.cursors.DictCursor)
except pymysql.Error as e:
    print e
    sys.exit(1)

table = prettytable.PrettyTable(border=True, header=True, left_padding_width=2, padding_width=1)
if connection is not None:
    with connection.cursor() as cursor:
        cursor.execute("show full processlist")
    field_names_list = list()
    for item in cursor:
        if isinstance(item, dict):
            row_data_list = list()
            for key, value in item.iteritems():
                field_names_list.append(key)
                row_data_list.append(value)
            table.add_row(row_data_list)
            del row_data_list
    table.field_names = field_names_list
    print table
