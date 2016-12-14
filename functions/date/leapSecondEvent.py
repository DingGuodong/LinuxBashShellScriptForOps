#!/usr/bin/python
# encoding: utf-8
# -*- coding: utf8 -*-
"""
Created by PyCharm.
File:               LinuxBashShellScriptForOps:leapSecondEvent.py
User:               Guodong
Create Date:        2016/12/13
Create Time:        10:00

Leap Second Issues
https://access.redhat.com/articles/15145


 """
import datetime
import time

print time.mktime(time.strptime('2011-12-31 23.59.60', '%Y-%m-%d %H.%M.%S'))
print time.mktime(time.strptime('2016-12-31 23.59.60', '%Y-%m-%d %H.%M.%S'))

print datetime.datetime.fromtimestamp(1325347200.0).strftime("%Y-%m-%d %H:%M:%S")
print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(1325347200.0))
print datetime.datetime.fromtimestamp(1483200000.0).strftime("%Y-%m-%d %H:%M:%S")
print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(1483200000.0))
