#!/usr/bin/python
# encoding: utf-8
# -*- coding: utf8 -*-
"""
Created by PyCharm.
File:               LinuxBashShellScriptForOps:portStatistics.py
User:               Guodong
Create Date:        2016/10/27
Create Time:        10:51

Note:
    Attention, This is a bad example, please see next version,
    reserve this version is for log and remember this stupid design.

    # python portStatistics.py
    Total connections of port 22 is 1.
    +-----+--------------+-------------------+-------------------+-----------------+--------------+
    | No. | Total Counts | Remote IP Address | Established Conns | Time_wait Conns | Others Conns |
    +-----+--------------+-------------------+-------------------+-----------------+--------------+
    |  1  |      1       |     10.6.28.46    |         1         |        0        |      0       |
    +-----+--------------+-------------------+-------------------+-----------------+--------------+
    Elapsed time: 0.00729203224182 seconds.
    #

 """

import psutil
import prettytable
import time

startTime = time.time()

port = 22  # ssh -i /etc/ssh/ssh_host_rsa_key root@10.6.28.28

# define data structure for each connection, each ip is unique unit
ipaddress = {
    'ipaddress': None,
    'counts': 0,
    'stat': {
        'established': 0,
        'time_wait': 0,
        'others': 0
    }
}

# define data structure for statistics
statistics = {
    'portIsUsed': False,
    'portUsedCounts': 0,
    'portPeerIpList': [],
    'portPeerList': [
        {
            'ipaddress': None,
            'counts': 0,
            'stat': {
                'established': 0,
                'time_wait': 0,
                'others': 0
            },
        },
    ]
}

tmp_portPeerList = list()
portPeerSet = set()

table = prettytable.PrettyTable()
table.field_names = ["No.", "Total Counts", "Remote IP Address", "Established Conns", "Time_wait Conns",
                     "Others Conns"]

netstat = psutil.net_connections()

for i, sconn in enumerate(netstat):

    if port in sconn.laddr:
        statistics['portIsUsed'] = True
        if len(sconn.raddr) != 0:
            statistics['portUsedCounts'] += 1
            ipaddress['ipaddress'] = sconn.raddr[0]
            ipaddress['counts'] += 1
            if sconn.status == 'ESTABLISHED':
                ipaddress['stat']['established'] += 1
            if sconn.status == 'TIME_WAIT':
                ipaddress['stat']['time_wait'] += 1
            tmp_portPeerList.append(str(ipaddress))  # dict() list() set() is unhashable type, collections.Counter

for ip in tmp_portPeerList:
    portPeerSet.add(str(ip))  # remove duplicated ip address using set()

for member in portPeerSet:
    statistics['portPeerList'].append(eval(member))

if statistics['portIsUsed']:
    print "Total connections of port %s is %d." % (port, statistics['portUsedCounts'])
    for i, ip in enumerate(statistics['portPeerList']):
        # print i, type(ip)
        if ip['ipaddress'] is not None:
            table.add_row([i, ip['counts'], ip['ipaddress'], ip['stat']['established'], ip['stat']['time_wait'],
                           ip['stat']['others']])
    print table.get_string(sortby=table.field_names[1], reversesort=True)
else:
    print 'port %s has no connections, please make sure port is listen or in use.' % port

endTime = time.time()
print "Elapsed time: %s seconds." % (endTime - startTime)
