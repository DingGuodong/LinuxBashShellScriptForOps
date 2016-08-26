#!/usr/bin/python
# encoding: utf-8
# -*- coding: utf8 -*-
"""
Created by PyCharm.
File:               LinuxBashShellScriptForOps:getSystemStatus.py
User:               Guodong
Create Date:        2016/8/18
Create Time:        15:32
 """
import platform
import psutil
import multiprocessing
import subprocess
import os
import time


def getHostname():
    return platform.node()


def getCPU():
    return [x / 100.0 for x in psutil.cpu_percent(interval=0, percpu=True)]


def getLoadAverage():
    k = 1.0
    k /= multiprocessing.cpu_count()
    if os.path.exists('/proc/loadavg'):
        return [float(open('/proc/loadavg').read().split()[x]) * k for x in range(3)]
    else:
        tokens = subprocess.check_output(['uptime']).split()
        return [float(x.strip(',')) * k for x in tokens[-3:]]


def getMemory():
    v = psutil.virtual_memory()
    return {
        'used': v.total - v.available,
        'free': v.available,
        'total': v.total
    }


def getUptime():
    uptime_file = "/proc/uptime"
    if os.path.exists(uptime_file):
        with open(uptime_file, 'r') as f:
            return f.read().split(' ')[0].strip("\n")
    else:
        return time.time() - psutil.boot_time()

