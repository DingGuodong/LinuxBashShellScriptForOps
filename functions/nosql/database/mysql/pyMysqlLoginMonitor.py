#!/usr/bin/python
# encoding: utf-8
# -*- coding: utf8 -*-
"""
Created by PyCharm.
File:               LinuxBashShellScriptForOps:pyMysqlLoginMonitor.py
User:               Guodong
Create Date:        2017/2/16
Create Time:        16:28
 """

import logging
import logging.handlers
import os
import time
import sys


class logger(object):
    def __init__(self, name=None, path=None, stream=True, level=logging.DEBUG):

        self.name = name if name else "default"

        if path and os.path.exists(path):
            path_to_logfile = path
        else:
            path_to_logfile = "/tmp"
        current_time = time.strftime("%Y%m%d")
        self.logfile = current_time + "_" + self.name + ".log"

        if not os.path.exists(path_to_logfile):
            os.makedirs(path_to_logfile)
        else:
            self.logfile = os.path.join(path_to_logfile, self.logfile)

        self.log = logging.getLogger(name=self.name)
        log_formatter = logging.Formatter("%(asctime)s %(filename)s:%(lineno)d %(name)s %(levelname)s: %(message)s",
                                          "%Y-%m-%d %H:%M:%S")
        file_handler = logging.handlers.RotatingFileHandler(self.logfile, maxBytes=104857600, backupCount=5)
        file_handler.setFormatter(log_formatter)

        self.log.addHandler(file_handler)
        if stream:
            stream_handler = logging.StreamHandler(sys.stderr)
            self.log.addHandler(stream_handler)
        self.log.setLevel(level)

    def debug(self, message):
        self.log.debug(message)

    def info(self, message):
        self.log.info(message)

    def warn(self, message):
        self.log.warning(message)

    def error(self, message):
        self.log.error(message)


log = logger(name="mysql_monitor", path="/tmp", stream=False, level=logging.INFO)


def mysql_query(sql):
    """
    mysql query sql on mysql server
    :param sql:  SQL
    :type sql: str
    :return result:  return all result with fetchall()
    :type: tuple
    """
    import pymysql
    try:
        connection = pymysql.connect(host='localhost', user='dev', passwd='dEvp@ssw0rd', db='test', port=3306,
                                     charset='utf8',
                                     read_timeout=10, write_timeout=10,
                                     cursorclass=pymysql.cursors.DictCursor)
    except pymysql.err.OperationalError as e:
        log.error("%s %s" % (e.args, e.message))
        sys.exit(1)

    try:
        with connection.cursor() as cursor:
            cursor.execute(sql)
        connection.commit()
    finally:
        connection.close()
    if cursor is not None:
        # fetchall() return a tuple
        return cursor.fetchall()
    else:
        print('This will never be reached when joined gevent')
        sys.exit(1)


def show_login_users_count(user=None):
    """
    this function is deprecated, use len(show_login_hosts) to get login user count
    :param user:
    :return:
    """
    if isinstance(user, str) and user != "":
        sql = r"SELECT count(ID) AS count FROM information_schema.PROCESSLIST WHERE USER='%s';" % user
    else:
        sql = r"SELECT count(ID) AS count FROM information_schema.PROCESSLIST WHERE ID IS NOT NULL;"
    tuple_users_count = mysql_query(sql)
    from collections import Iterable
    if len(tuple_users_count) != 0 and isinstance(tuple_users_count, Iterable):
        for item in tuple_users_count:
            return item['count']
    else:
        return 0


def show_login_hosts(user=None):
    """
    show hosts login, return a list, such as
    :param user:
    :return
    :type: list
    """
    if isinstance(user, str) and user != "":
        sql = r"SELECT `HOST` AS hosts FROM information_schema.PROCESSLIST WHERE USER='%s';" % user
    else:
        sql = r"SELECT `HOST` AS hosts FROM information_schema.PROCESSLIST WHERE ID IS NOT NULL;"
    tuple_login_hosts = mysql_query(sql)
    from collections import Iterable
    if len(tuple_login_hosts) != 0 and isinstance(tuple_login_hosts, Iterable):
        list_hosts = list()
        for item in tuple_login_hosts:
            list_hosts.append(item["hosts"])
        return list_hosts if list_hosts else []
    else:
        return []


def show_login_hosts_statistics(user=None):
    """
    show statistics information about hosts login, return host and login times in dict type
    :param user:
    :return:
    """
    list_login_hosts = show_login_hosts(user)
    if True in [item.find("::1") == 0 for item in list_login_hosts]:
        list_login_hosts = [item.replace("::1", "127.0.0.1") for item in list_login_hosts]
    from collections import Counter
    return Counter(item.split(":")[0] for item in list_login_hosts)


if __name__ == '__main__':
    # TODO(Guodong Ding) list_hosts_is_allowed, enable * or % in list. such as 172.17.0.* or 172.17.0.%
    list_hosts_is_allowed = ["::1", "127.0.0.1", "localhost"]
    hosts = show_login_hosts_statistics(user='dev')

    error_flag = True

    for host in hosts:
        if host not in list_hosts_is_allowed:
            log.error("%s is not allowed login, but it did" % host)
            error_flag = True
        else:
            error_flag = False

    if error_flag:
        print(1)
    else:
        print(0)
