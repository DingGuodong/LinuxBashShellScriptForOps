#!/usr/bin/python
# encoding: utf-8
# -*- coding: utf8 -*-
"""
Created by PyCharm.
File:               LinuxBashShellScriptForOps:netstat.py
User:               Guodong
Create Date:        2017/1/16
Create Time:        17:38
 """
import psutil

for c in psutil.net_connections(kind='inet'):
    if c.laddr[1] == 80:
        print(c)
