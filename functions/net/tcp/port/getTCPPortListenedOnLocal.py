#!/usr/bin/python
# encoding: utf-8
# -*- coding: utf8 -*-
"""
Created by PyCharm.
File Name:              LinuxBashShellScriptForOps:getTCPPortListenedOnLocal.py
Version:                0.0.1
Author:                 Guodong
Author Email:           dgdenterprise@gmail.com
URL:                    https://github.com/DingGuodong/LinuxBashShellScriptForOps
Download URL:           https://github.com/DingGuodong/LinuxBashShellScriptForOps/tarball/master
Create Date:            2017/11/9
Create Time:            17:25
Description:            
Long Description:       
References:             
Prerequisites:          yum install python-devel
                        pip install --upgrade pip
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
import json
from collections import OrderedDict

import psutil


class ZabbixLLDNetConnections(object):
    def __init__(self):
        self.status_set = [
            "ESTABLISHED",
            "SYN_SENT",
            "SYN_RECV",
            "FIN_WAIT1",
            "FIN_WAIT2",
            "TIME_WAIT",
            "CLOSE",
            "CLOSE_WAIT",
            "LAST_ACK",
            "LISTEN",
            "CLOSING",
            "NONE",
        ]  # do not use 'set'(var={'xxx',}) here for < Python 2.6
        # https://docs.python.org/2/library/stdtypes.html#set
        # As of Python 2.7, non-empty sets (not frozensets) can be created by placing a comma-separated list
        # of elements within braces, for example: {'jack', 'sjoerd'}, in addition to the set constructor.
        self.status_cared = [
            'ESTABLISHED',
            'TIME_WAIT',
            'CLOSE_WAIT',
        ]  # do not use 'set'(var={'xxx',}) here for < Python 2.6
        self.net_connections_raw_iterable_object = psutil.net_connections()
        self.port_list = self.get_tcp_port_listened_local()
        self.port_pid_dict = self.get_port_pid_map()

        self.data = self.get_zabbix_lld_json()

    def get_tcp_port_listened_local(self):
        port_listened = set()
        for conn in self.net_connections_raw_iterable_object:
            if conn.status == 'LISTEN':
                port_listened.add(conn.laddr[1])
        return sorted(port_listened)

    def get_tcp_port_pid(self, port):
        port_pid_dict = dict()
        port_to_filter = port
        for conn in self.net_connections_raw_iterable_object:
            if conn.laddr[1] == port_to_filter:
                port_pid_dict[port] = conn.pid
        return port_pid_dict

    def get_tcp_port_status_count(self, port, status):
        count = 0
        port_to_filter = port
        status_to_filter = status
        for conn in self.net_connections_raw_iterable_object:
            if conn.laddr[1] == port_to_filter and conn.status == status_to_filter:
                count += 1
        return count

    def get_tcp_port_statics(self, port):
        statics = OrderedDict()
        for status in self.status_cared:
            statics[status] = self.get_tcp_port_status_count(port, status)
        return dict(statics)

    def get_port_pid_map(self):
        port_pid_dict = dict()
        for port in self.port_list:
            port_pid_dict = dict(port_pid_dict, **self.get_tcp_port_pid(port))
        return port_pid_dict

    def get_zabbix_lld_json(self):
        data_list = list()
        for port in self.port_list:
            data_unit = dict()
            data_unit["{#PORT}"] = str(port)
            data_unit["{#PID}"] = str(self.port_pid_dict[port])
            data_unit["{#ESTABLISHED}"] = str(self.get_tcp_port_statics(port)["ESTABLISHED"])
            data_unit["{#TIME_WAIT}"] = str(self.get_tcp_port_statics(port)["TIME_WAIT"])
            data_unit["{#CLOSE_WAIT}"] = str(self.get_tcp_port_statics(port)["CLOSE_WAIT"])
            data_list.append(data_unit)
        return json.dumps({"data": data_list}, indent=4)


if __name__ == '__main__':
    nc = ZabbixLLDNetConnections()
    print nc.data
