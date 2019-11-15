#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created by PyCharm.
File Name:              LinuxBashShellScriptForOps:monitor_tcp_status.py
Version:                0.0.1
Author:                 dgden
Author Email:           dgdenterprise@gmail.com
URL:                    https://github.com/DingGuodong/LinuxBashShellScriptForOps
Download URL:           https://github.com/DingGuodong/LinuxBashShellScriptForOps/tarball/master
Create Date:            2019/11/15
Create Time:            13:59
Description:            TCP status monitoring with python
Long Description:       designed for zabbix
References:             
Prerequisites:          pip install ipy
                        pip install psutil
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

import psutil
from IPy import IP

sconn_list = psutil.net_connections(kind='tcp')

TCP_STATUS_TYPE_LIST = ['LISTEN', 'SYN_SENT', 'ESTABLISHED', 'FIN_WAIT1', 'CLOSE_WAIT', 'FIN_WAIT2', 'TIME_WAIT', ]


def __get_sconn_status_set():
    sconn_status_set = set()
    for sconn in sconn_list:
        sconn_status_set.add(sconn.status)

    print sconn_status_set


def is_private_ipv4(ip):
    if IP(ip).iptype() == "PRIVATE":
        return True
    else:
        return False


def get_all_tcp_conn_count_by_status(status='ESTABLISHED'):
    status = status.upper()
    if status not in TCP_STATUS_TYPE_LIST:
        return 0
    else:
        return len([sconn for sconn in sconn_list if sconn.status == status])


def get_private_tcp_conn_count_established():
    return len([sconn for sconn in sconn_list if sconn.status == 'ESTABLISHED' and is_private_ipv4(sconn.raddr.ip)])


if __name__ == '__main__':
    if len(sys.argv) == 1:
        for tcp_status_type in TCP_STATUS_TYPE_LIST:
            print(tcp_status_type, get_all_tcp_conn_count_by_status(tcp_status_type))
        print('P_ESTABLISHED', get_private_tcp_conn_count_established())
    elif len(sys.argv) == 2:
        print(get_all_tcp_conn_count_by_status(sys.argv[1]))
    else:
        raise RuntimeError("bad call")
