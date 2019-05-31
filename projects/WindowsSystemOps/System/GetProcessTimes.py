#!/usr/bin/python
# encoding: utf-8
# -*- coding: utf8 -*-
"""
Created by PyCharm.
File:               LinuxBashShellScriptForOps:GetProcessTimes.py
User:               Guodong
Create Date:        2016/8/30
Create Time:        17:22
 """

# TODO(Guodong Ding): process create time got is not right, maybe a bug from psutil module

import time
import psutil
import sys


def uptime(seconds):
    SECOND = 1
    MINUTE = SECOND * 60
    HOUR = MINUTE * 60
    DAY = HOUR * 24
    days, mod = divmod(seconds, DAY)
    hours, mod = divmod(mod, HOUR)
    minutes, seconds = divmod(mod, MINUTE)
    result = (days, hours, minutes, seconds)
    result = [int(round(x)) for x in result]
    return result


processName = "named"

processCreateTime = None

for p in psutil.process_iter():
    if "named.exe" in p.name():
        processCreateTime = p.create_time()
        processObject = p

if processCreateTime is None:
    sys.stderr.write("%s is not running, or bad command name." % processName)
    sys.exit(1)
else:
    boot_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(processCreateTime))
    now_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    up_time = uptime(time.time() - processCreateTime)
    print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(psutil.boot_time())))
    print(processObject.pid, "%s up %d days, %d:%d" % (now_time, up_time[0], up_time[1], up_time[2]))
