#!/usr/bin/python
# encoding: utf-8
# -*- coding: utf8 -*-
"""
Created by PyCharm.
File:               LinuxBashShellScriptForOps:py-centos6-init.py
User:               Guodong
Create Date:        2016/9/9
Create Time:        11:20
 """

from fabric.api import *
from fabric.colors import *
from fabric.context_managers import *
import ipaddress
import re
import sys

#  discovery live hosts on LAN using python
#  nmap -sn 10.6.28.0/24
#  nmap -sP -PS22 10.6.28.0/24

ping_result = ""
ping_network = "192.168.1."


def exec_local_cmd(cmd):
    # with settings(warn_only=True):
    with hide('output', 'running', 'warnings'), settings(warn_only=True):
        return local(cmd, capture=True)


for num in range(1, 24):
    result = str(exec_local_cmd("ping -n1 " + ping_network + str(num)))
    print result.decode(sys.getfilesystemencoding()).encode(encoding='utf-8')
    if result:
        print ping_network + str(num)
    else:
        continue

sys.exit(0)

nmap_result = ""

pattern_ip = r'(?<![\.\d])(?:\d{1,3}\.){3}\d{1,3}(?![\.\d])'
pattern = re.compile(pattern_ip)
match = pattern.findall(nmap_result)
if match:
    for ip in match:
        try:
            print ipaddress.IPv4Address(unicode(ip))
        except ipaddress.AddressValueError:
            pass
