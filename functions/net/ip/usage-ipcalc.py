#!/usr/bin/python
# encoding: utf-8
# -*- coding: utf8 -*-
"""
Created by PyCharm.
File:               LinuxBashShellScriptForOps:usage-ipcalc.py.py
User:               Guodong
Create Date:        2017/4/30
Create Time:        10:46
 """
import IPy

import ipcalc
# https://pypi.python.org/pypi/ipcalc/1.99.0
# Note: ipcalc is a program come from Linux package 'ipcalc'

import pyipcalc

# Another module
# https://pypi.python.org/pypi/pyipcalc/1.0.1

print ipcalc.IP("192.168.1.1")
print ipcalc.IP("192.168.1.1/24").info()  # PRIVATE
print ipcalc.IP("124.129.14.90/30").mask

print ipcalc.Network('192.168.1.0/24')
print ipcalc.Network('192.168.1.0/255.255.255.0')

print pyipcalc.IPNetwork("192.168.1.0/24").mask()  # better than ipcalc
print pyipcalc.IPNetwork("192.168.1.0/24").network()

ip_str = '''192.168.4.1
192.168.4.3
192.168.4.4
192.168.6.54
192.168.6.55
192.168.6.100
192.168.6.101
'''
ip_list = ip_str.strip().split('\n')
ip_network_list = list()
for ip in ip_list:
    if len(ip.strip().split('/')) != 2:
        ip = ip + '/24'
    ip_network_list.append(pyipcalc.IPNetwork(ip).network())
ip_network_uniq_list = set(ip_network_list)

ip_network_list2 = list()
for ip in ip_list:
    if len(ip.strip().split('/')) != 2:
        ip = ip + '/32'
    ip_network_list2.append(IPy.IP(ip).net())
ip_network_uniq_list2 = set(ip_network_list2)
print ip_network_uniq_list2
