#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created by PyCharm.
File Name:              LinuxBashShellScriptForOps:get-all-nginx-clients-ip.py
Version:                0.0.1
Author:                 dgden
Author Email:           dgdenterprise@gmail.com
URL:                    https://github.com/DingGuodong/LinuxBashShellScriptForOps
Download URL:           https://github.com/DingGuodong/LinuxBashShellScriptForOps/tarball/master
Create Date:            2019/10/22
Create Time:            18:23
Description:            get clients that establishes an active connection to nginx
Long Description:       将Linux服务器中nginx的客户端连接信息（仅限IPv4）打印出来
                        要求：不含nginx与upstream和自身listen的连接信息

References:
    Sehll脚本实现：
        ports=$(netstat -nlpt|awk '/LISTEN/&&/nginx/'|awk '{print$4}'|awk -F: '{print$2}')
        for port in $ports;do netstat -anopt|awk "/nginx/&&/ESTABLISHED/&&\$4~/:$port$/";done

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

import os

import psutil


def get_all_nginx_clients_ip(data_source):
    # type: (list) -> None
    # one line version
    print "".join(filter(
        lambda row: True if row.strip().split()[3].split(":")[1] in [line.strip().split()[3].split(":")[1] for line in
                                                                     filter(lambda x: True if 'LISTEN' in x else False,
                                                                            data_source)] else False,
        filter(lambda x: True if 'LISTEN' not in x else False, data_source)))


def get_all_nginx_clients_ip_for_human(data_source):
    # type: (list) -> None
    # easy to read friendly version
    all_listened_lines_list = filter(lambda x: True if 'LISTEN' in x else False, data_source)

    all_listened_ports_list = [line.strip().split()[3].split(":")[1] for line in all_listened_lines_list]

    all_establish_lines_list = filter(lambda x: True if 'LISTEN' not in x else False, data_source)
    all_nginx_clients_ip_list = filter(
        lambda row: True if row.strip().split()[3].split(":")[1] in all_listened_ports_list else False,
        all_establish_lines_list)

    print "".join(all_nginx_clients_ip_list)


def sort_list_by_column(iterable, split_by=" ", column=0, reverse=True):
    return sorted(iterable, key=lambda x: x.strip().split(split_by)[column], reverse=reverse)


def get_nginx_pids_list():
    for process in psutil.process_iter():
        if process.name() == 'nginx':
            yield process.pid


def get_nginx_listened_ports():
    for connection in psutil.net_connections(kind='tcp4'):
        if connection.status == "LISTEN" and connection.pid in [x.pid for x in psutil.process_iter() if
                                                                x.name() == 'nginx']:
            yield connection.laddr.port


def get_nginx_established_conn_list():
    nginx_pids_list = [x for x in get_nginx_pids_list()]
    nginx_listened_ports_list = [x for x in get_nginx_listened_ports()]
    for connection in psutil.net_connections(kind='tcp4'):
        if connection.status != "LISTEN" \
                and connection.pid in nginx_pids_list \
                and connection.laddr.port in nginx_listened_ports_list:
            print connection


if __name__ == '__main__':
    DEMO_DATA_SOURCE_FILE_01 = 'netstat_anopt_20191022_prod_nginx01.txt'  # netstat -anopt |grep nginx > ngx01.txt

    if os.path.exists(DEMO_DATA_SOURCE_FILE_01):
        with open(DEMO_DATA_SOURCE_FILE_01, 'r') as fp:
            demo_data_source_01 = fp.readlines()
        get_all_nginx_clients_ip_for_human(demo_data_source_01)
    else:
        get_nginx_established_conn_list()
