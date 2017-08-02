#!/usr/bin/python
# encoding: utf-8
# -*- coding: utf8 -*-
"""
Created by PyCharm.
File:               LinuxBashShellScriptForOps:pyTcpConnStatistics.py
User:               Guodong
Create Date:        2017/7/31
Create Time:        9:48
Description:        TCP Connection Statistic
References:         
 """
import collections
import psutil

net_connections = psutil.net_connections(kind='tcp')

# print TCP connections statistics, total conns, listen counts, close wait counts, established counts, time wait counts
counter = collections.Counter()
for item in net_connections:
    counter['total_conn'] += 1
    if item.status == 'LISTEN':
        counter['num_listen'] += 1
    if item.status == 'ESTABLISHED':
        counter['num_est'] += 1
    if item.status == 'TIME_WAIT':
        counter['num_tw'] += 1
    if item.status == 'CLOSE_WAIT':
        counter['num_cw'] += 1
print counter

# print opened counts for each opened TCP port
listen_ports = sorted(set([item.laddr[1] for item in net_connections if item.status == 'LISTEN']), reverse=False)
port_counter = collections.Counter()
for item in net_connections:
    if item.laddr[1] in listen_ports:
        port_counter[item.laddr[1]] += 1
print sorted(port_counter.iteritems(), key=lambda x: x[1], reverse=True)  # 'key=lambda x: x[1]' means sort by value

# print opened counts for each opened TCP port, Top 5
tcp_conns_top_5 = sorted(port_counter.iteritems(), key=lambda x: x[1], reverse=True)[:5]  # TCP conns top 5
print tcp_conns_top_5

# print opened counts for each opened TCP port, Top 5, include port, pid and process name
port_pid_mapper = dict()
for item in net_connections:
    if item.laddr[1] in listen_ports and item.status == 'LISTEN':
        port_pid_mapper[item.laddr[1]] = item.pid

port_pid_process_mapper = list()
for port, pid in port_pid_mapper.iteritems():
    if port in [member[0] for member in tcp_conns_top_5]:
        port_pid_process_mapper += [(port, proc.pid, proc.name()) for proc in psutil.process_iter() if proc.pid == pid]

# a hard way to sort 'port_pid_process_mapper' list by 'tcp_conns_top_5' list
port_pid_process_mapper_sorted = list()
for item in tcp_conns_top_5:
    port_pid_process_mapper_sorted += [member for member in port_pid_process_mapper if member[0] == item[0]]

print port_pid_process_mapper_sorted

# a easy way to sort 'port_pid_process_mapper' list by 'tcp_conns_top_5' list, using dict to store sequence of item
# PEP 274 -- Dict Comprehensions, https://www.python.org/dev/peps/pep-0274/
port_pid_process_mapper_dict = {item[0]: tcp_conns_top_5.index(item) for item in tcp_conns_top_5}
print sorted(port_pid_process_mapper, key=lambda x: port_pid_process_mapper_dict[x[0]])
