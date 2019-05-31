#!/usr/bin/python
# encoding: utf-8
# -*- coding: utf8 -*-
"""
Created by PyCharm.
File:               LinuxBashShellScriptForOps:pyTestMysqlConnection.py
User:               Guodong
Create Date:        2016/12/20
Create Time:        11:53

Example of program test if can connect to MySQL server
Usage:
  pyTestMysqlConnection.py [-h hostname] [-u username] [-p password] [-P port] [DATABASE] [SQL]
  pyTestMysqlConnection.py [--host=hostname] [--user=username] [--password=password] [--port=port] [database] [SQL]
  pyTestMysqlConnection.py --version | -v
  pyTestMysqlConnection.py --help | -?

Arguments:
  DATABASE                          mysql server database
  SQL                               sql statement

Options:
  -? --help                         show this help message and exit
  -v --version                      show version and exit
  -h hostname --host=hostname       Connect to host [default: localhost]
  -u username --user=username       User for login if not current user [default: root]
  -p password --password=password   Password to use when connecting to server
                                    If password is not given it's asked from the tty
  -P port --port=port               Port number to use for connection [default: 0]

 """

import getpass
import sys

import pymysql
# https://github.com/docopt/docopt/tree/master/examples
# https://github.com/docopt/docopt/blob/master/examples/options_example.py
from docopt import docopt


def mysql_connect(host, user, password, port, charset, database):
    try:
        connection = pymysql.connect(host=host, user=user, password=password, database=database, port=port,
                                     charset=charset,
                                     cursorclass=pymysql.cursors.DictCursor, connect_timeout=5)
        if connection:
            return connection
    except pymysql.Error as e:
        # raise RuntimeError("Can't connect to MySQL server")
        print(e)
        return None


def mysql_query(host, user, password, port, charset, database, sql):
    try:
        connection = pymysql.connect(host=host, user=user, password=password, database=database, port=port,
                                     charset=charset,
                                     cursorclass=pymysql.cursors.DictCursor, connect_timeout=5)
    except pymysql.Error as e:
        # raise RuntimeError("Can't connect to MySQL server")
        print(e)
        sys.exit(1)

    try:
        with connection.cursor() as cursor:
            cursor.execute(sql)
        connection.commit()
    finally:
        connection.close()
    if cursor is not None:
        return cursor
    else:
        sys.exit(1)


mswindows = (sys.platform == "win32")  # learning from 'subprocess' module

host = ''
username = user = ''
password = passwd = ''
database = db = ''
port = 0
charset = 'utf8'
sql = ''

if __name__ == '__main__':
    # user option setting
    arguments = docopt(__doc__, version='1.0.0rc2')

    if arguments['--host'] is not None or arguments['--host'] != "":
        host = arguments['--host']

    if arguments['--user'] is not None or arguments['--user'] != "":
        username = arguments['--user']
    else:
        username = getpass.getuser()  # this cannot be reached, because '[default: root]' in __doc__

    if arguments['--password'] is None or arguments['--password'] == "":
        while True:
            password = getpass.getpass("Enter password: ")
            if password != "" and password is not None:
                break
            else:
                print("MySQL password is empty will not be safe")
    else:
        password = arguments['--password']
    if arguments['DATABASE'] is not None and arguments['DATABASE'] != "":
        database = arguments['DATABASE']
    if arguments['SQL'] is not None and arguments['SQL'] != "":
        sql = arguments['SQL']

    # main
    result = None
    if mswindows:
        import socket

        # global socket timeout
        socket.setdefaulttimeout(10.0)
        result = mysql_connect(host, username, password, port, charset, database)
    else:
        assert sys.platform == "linux2", "please run this script on Windows or Linux"
        from timeout import timeout

        with timeout(timeout=10.0):
            result = mysql_connect(host, username, password, port, charset, database)
    if result:
        print("connect to MySQL server successfully!")
    else:
        print("Can't connect to MySQL server")
        sys.exit(1)
