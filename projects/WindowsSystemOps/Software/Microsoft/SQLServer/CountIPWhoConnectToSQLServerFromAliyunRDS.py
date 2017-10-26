#!/usr/bin/python
# encoding: utf-8
# -*- coding: utf8 -*-
"""
Created by PyCharm.
File:               LinuxBashShellScriptForOps:CountIPWhoConnectToSQLServerFromAliyunRDS.py
User:               Guodong
Create Date:        2017/8/15
Create Time:        10:15
Description:        Python Connect to Aliyun RDS SQL Server on Windows With pymssql with connection statistics
References:
 """
import collections
import os
import pymssql  # Python Connect to Aliyun RDS SQL Server on Windows
import shelve  # Manage shelves of pickled objects
import time


def get_system_encoding():
    import codecs
    import locale
    """
    The encoding of the default system locale but falls back to the given
    fallback encoding if the encoding is unsupported by python or could
    not be determined.  See tickets #10335 and #5846
    """
    try:
        encoding = locale.getdefaultlocale()[1] or 'ascii'
        codecs.lookup(encoding)
    except Exception as _:
        del _
        encoding = 'ascii'
    return encoding


DEFAULT_LOCALE_ENCODING = get_system_encoding()


def get_connection_detail():
    server = 'rdsid.sqlserver.rds.aliyuncs.com'
    port = "3433"
    username = 'db_username'
    password = 'db_password'

    conn = pymssql.connect(server=server, port=port, user=username, password=password, timeout=5)
    cursor = conn.cursor()
    cursor.execute("""
    SELECT connection_id,
            login_time, 
            connect_time,
            hostname, 
            net_library, 
            net_address, 
            client_net_address,
            program_name,
            loginame,
            last_read,
            last_write
    FROM    sys.sysprocesses AS S 
    INNER JOIN    sys.dm_exec_connections AS decc ON S.spid = decc.session_id 
    WHERE   spid  IN (SELECT spid FROM 
    [MASTER].[dbo].[SYSPROCESSES] WHERE [DBID] IN ( SELECT 
       [DBID] 
    FROM 
       [MASTER].[dbo].[SYSDATABASES]))
    """)

    row = cursor.fetchone()
    result_list = list()
    while row:
        result_list.append(row)
        row = cursor.fetchone()
    conn.close()
    return result_list


if __name__ == '__main__':
    """
    Example outputs:
    lookup clients connected to sql server, please keeping wait... 
    There are 282 logs was recorded during 50 seconds.
    There are 4 SQL Server Clients using Aliyun RDS:
    IP Address: xxx.xxx.xxx.xxx, connection times: 99
    IP Address: xxx.xxx.xxx.xxx, connection times: 99
    IP Address: xxx.xxx.xxx.xxx, connection times: 51
    IP Address: xxx.xxx.xxx.xxx, connection times: 33
    Current connections:
    ... ...
    --end--
    """
    tmp_db = "__tmp.db"

    # create persistent object to save persistent data
    if not os.path.exists(tmp_db):
        persistent_object = shelve.open(tmp_db)
        persistent_object["connection_detail"] = list()  # save data into persistent object
        persistent_object.close()

    # save persistent data into persistent db
    persistent_object = shelve.open(tmp_db)
    keep_running_flag = True
    run_times = 0
    run_times_max = 24 * 3600 / 600
    sleep_seconds = 600
    print "lookup clients connected to sql server, please keeping wait... "
    while keep_running_flag:
        persistent_object["connection_detail"] += get_connection_detail()
        time.sleep(sleep_seconds)
        keep_running_flag = True if run_times < run_times_max else False
        run_times += 1
    persistent_object.close()

    # read data from persistent db
    persistent_object = shelve.open(tmp_db)
    print "There are {count} connections was recorded during {seconds} seconds.".format(
        count=len(persistent_object["connection_detail"]), seconds=run_times_max * sleep_seconds)

    # counting the counts of ip logged in sql server
    clients = collections.Counter()
    for record in persistent_object["connection_detail"]:
        clients[record[6]] += 1

    # get unique ip to connected to sql server and its connection times
    unique_clients_list = set()
    for record in persistent_object["connection_detail"]:
        unique_clients_list.add(record[6])
    print "There are {count} SQL Server Clients using Aliyun RDS:".format(count=len(unique_clients_list))
    for ip in unique_clients_list:
        print "IP Address: {ip}, connection times: {times}".format(ip=ip, times=clients[ip])
    persistent_object.close()

    # print current connections
    print "Current connections:"
    for connection in get_connection_detail():
        print connection
    print "--end--"
