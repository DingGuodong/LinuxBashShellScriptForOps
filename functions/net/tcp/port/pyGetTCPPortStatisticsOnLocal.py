#!/usr/bin/python
# encoding: utf-8
# -*- coding: utf8 -*-
"""
Created by PyCharm.
File Name:              LinuxBashShellScriptForOps:pyGetTCPPortStatisticsOnLocal.py
Version:                0.0.1
Author:                 Guodong
Author Email:           dgdenterprise@gmail.com
URL:                    https://github.com/DingGuodong/LinuxBashShellScriptForOps
Download URL:           https://github.com/DingGuodong/LinuxBashShellScriptForOps/tarball/master
Create Date:            2017/11/27
Create Time:            14:30
Description:            TCP connections statistics with Python
Long Description:       python 统计词频,python 统计出现次数 using 'Counter' from collections or 'dict' with self increase
References:             
Prerequisites:          psutil
Development Status:     3 - Alpha, 5 - Production/Stable
Environment:            Console
Intended Audience:      System Administrators, Developers, End Users/Desktop
License:                Freeware, Freely Distributable
Natural Language:       English, Chinese (Simplified)
Operating System:       POSIX :: Linux, Microsoft :: Windows

Topic:                  Utilities
 """
from collections import \
    Counter  # Counter is only supported python2.7 and higher and is not available in earlier versions.
from collections import OrderedDict

import psutil

# different functions use the same netstat result in case of wrong data
netstat = psutil.net_connections(kind="tcp")


def get_tcp_all_conns_count_top(top=10):
    cared_data = list()

    for sconn in netstat:
        cared_data.append((sconn.laddr[0], sconn.laddr[1]))

    cared_data_with_counter = Counter(cared_data)

    if len(cared_data) < top:
        top = len(cared_data)

    tcp_conns_top_x = sorted(iter(cared_data_with_counter.items()), key=lambda x: x[1], reverse=True)

    return tcp_conns_top_x[0:top]


def get_tcp_port_conns_count(port=1080):
    filtered_data = [sconn for sconn in netstat if sconn.laddr[1] == port and sconn.status != 'LISTEN']

    cared_data = OrderedDict()

    for _sconn in filtered_data:
        cared_data.setdefault(_sconn.raddr[0], {"ESTABLISHED": 0, "TIME_WAIT": 0, "CLOSE_WAIT": 0, "TOTAL": 0})
        try:
            cared_data[_sconn.raddr[0]][_sconn.status] += 1  # if ip's conn state is same, then its count plus 1
        except KeyError:
            # such as 'SYN_RECV' not involved
            pass

        if cared_data[_sconn.raddr[0]]["TOTAL"] == 0:  # use this statement to improve performance
            cared_data[_sconn.raddr[0]]["TOTAL"] = len(
                [x for x in filtered_data if x.raddr[0] == _sconn.raddr[0]])

    return {
        port: cared_data
    }


if __name__ == '__main__':
    import json

    # print port statistics of port listened on local host, sort by connection number
    # such as:
    # (('192.168.88.32', 993), 206)
    # (('192.168.88.32', 10050), 130)
    # (('192.168.88.32', 21836), 75)

    for item in get_tcp_all_conns_count_top():
        print(item)

    # print port statistics of each connected IP
    # such as:
    # {
    #     "21658": {
    #         "192.168.88.102": {
    #             "ESTABLISHED": 2,
    #             "TIME_WAIT": 0,
    #             "CLOSE_WAIT": 0
    #         },
    # ... ...
    # }
    s = get_tcp_all_conns_count_top(top=5)
    for conn in s:
        print(json.dumps(get_tcp_port_conns_count(port=conn[0][1]), indent=4))
