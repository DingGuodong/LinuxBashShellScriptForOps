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
    print processCreateTime
    print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(processCreateTime))
    print processObject.pid
