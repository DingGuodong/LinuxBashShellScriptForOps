#!/usr/bin/python
# encoding: utf-8
# -*- coding: utf8 -*-
"""
Created by PyCharm.
File:               LinuxBashShellScriptForOps:ServiceControl.py
User:               Guodong
Create Date:        2016/10/14
Create Time:        17:57
 """
import os
import sys
import socket
import win32serviceutil

serviceName = 'MySQL56'

hostname = socket.gethostname()

# win32serviceutil.StartService(serviceName)

statusCode = {
    0: "",
    1: "STOPPED",
    2: "START_PENDING",
    3: "STOP_PENDING",
    4: "RUNNING"
}

status = win32serviceutil.QueryServiceStatus(serviceName)[1]
print "service %s state is: %s" % (serviceName, statusCode[status])

# TODO(Guodong Ding) run a command as administrator with administrative privilege
state_command = "C:\WINDOWS\System32\sc.exe query MySQL56"
start_command = 'runas /user:administrator /savecred "C:\WINDOWS\System32\sc.exe start MySQL56"'
stop_command = "C:\WINDOWS\System32\sc.exe query MySQL56"
os.system(start_command)
print start_command
