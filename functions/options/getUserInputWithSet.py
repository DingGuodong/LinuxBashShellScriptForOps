#!/usr/bin/python
# encoding: utf-8
# -*- coding: utf8 -*-
"""
Created by PyCharm.
File:               LinuxBashShellScriptForOps:getUserInput.py
User:               Guodong
Create Date:        2016/9/29
Create Time:        11:11
 """
from IPy import IP

hosts = set()
while True:
    try:
        hosts.add(IP(raw_input('Please input ip address which host to xxx:'), ipversion=4))
    except ValueError, e:
        print "Please input a valid IP address."
        want_continue = raw_input("Continue? y/n <default is NO>")
        if want_continue in ['Yes', 'YES', 'yes', 'Y', 'y']:
            continue
        else:
            break

print hosts
