#!/usr/bin/python
# encoding: utf-8
# -*- coding: utf8 -*-
"""
Created by PyCharm.
File:               LinuxBashShellScriptForOps:pyCrontabKillProcess.py
User:               Guodong
Create Date:        2016/9/14
Create Time:        14:43
 """
import signal
import time
import sys


def kill_tail(sig_num, fram):
    print 'receive %s! timeout! exit!' % sig_num
    sys.exit(0)


# posix system support only
signal.signal(signal.SIGALRM, kill_tail)

signal.alarm(10)

t = 0
while 1:
    print "%s second" % t
    time.sleep(1)
    t += 1
