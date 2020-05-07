#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created by PyCharm.
File Name:              LinuxBashShellScriptForOps:pyExecuteSqlScriptFile.py
Version:                0.0.1
Author:                 Guodong
Author Email:           dgdenterprise@gmail.com
URL:                    https://github.com/DingGuodong/LinuxBashShellScriptForOps
Download URL:           https://github.com/DingGuodong/LinuxBashShellScriptForOps/tarball/master
Create Date:            2019/4/15
Create Time:            13:38
Description:            execute SQL statements in a script file (batch file)
Long Description:       
References:             mysql db_name < script.sql > output.tab

                        https://stackoverflow.com/a/36121851
                        the cursor.execute() method is designed take only one statement,
                        because it makes guarantees about the state of the cursor afterward.
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


def mysql_query(host='127.0.0.1', user='dev', password='dEvp@ssw0rd', database='test', port=3306,
                charset='utf8', sql="show databases;"):
    """
    query one sql statement, and print result
    :param host:
    :param user:
    :param password:
    :param database:
    :param port:
    :param charset:
    :param sql: str, one sql statement, sql.count(";") <= 1
    :return:
    """
    if sql.count(";") > 1 or sql.strip().strip(";").count(";") > 0:
        raise SyntaxError("the cursor.execute() method is designed take only one statement")

    try:
        connection = pymysql.connect(host=host, user=user, passwd=password, db=database, port=port,
                                     charset=charset,
                                     cursorclass=pymysql.cursors.DictCursor)
    except pymysql.Error as e:
        print(e)
        sys.exit(1)

    table = prettytable.PrettyTable(border=True, header=True, left_padding_width=0, padding_width=0)
    if connection is not None:
        with connection.cursor() as cursor:
            cursor.execute(sql)
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
        return table


def mysql_execute_sql_file(host='127.0.0.1', user='dev', password='dEvp@ssw0rd', database='test', port=3306,
                           charset='utf8mb4', sql="show databases;"):
    """
    query multilines sql statements(execute SQL file) and no print as import
    :param host:
    :param user:
    :param password:
    :param database:
    :param port:
    :param charset:
    :param sql: str
    :return:
    """
    connection = None
    try:
        connection = pymysql.connect(host=host, user=user, passwd=password, db=database, port=port,
                                     charset=charset,
                                     cursorclass=pymysql.cursors.SSCursor)

        if connection is not None:
            with connection.cursor() as cursor:
                if ";" in sql:
                    # https://stackoverflow.com/a/36121851
                    # the cursor.execute() method is designed take only one statement,
                    # because it makes guarantees about the state of the cursor afterward.
                    for line in sql.strip().strip(";").split(";"):
                        # this line may raise pymysql.Error when in some special SQL statement,
                        # such as the SQL contain some special character. e.g. 'phpbb_bbcodes'
                        cursor.execute(line)
                else:
                    cursor.execute(sql)
        connection.commit()
    except pymysql.Error as e:
        print(e)
        sys.exit(1)

    finally:
        if connection is not None:
            connection.close()


if __name__ == '__main__':
    print(mysql_query(sql="show full processlist"))

    import os

    if os.path.exists("test.sql"):
        with open("test.sql") as fp:
            mysql_execute_sql_file(sql=fp.read())
