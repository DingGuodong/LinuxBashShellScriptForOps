#!/usr/bin/python
# encoding: utf-8
# -*- coding: utf8 -*-
"""
Created by PyCharm.
File:               LinuxBashShellScriptForOps:resetPrinterSpoolerService.py
User:               Guodong
Create Date:        2017/9/7
Create Time:        15:07
Description:        reset Windows printer spooler service to make printers work again
References:         
 """
import win32serviceutil
import os
import sys

service_name = 'spooler'.capitalize()
path = r"C:\Windows\System32\spool\PRINTERS"

print "reset printer spooler service in progress ..."

if os.path.exists(path):
    if os.listdir(path):
        print "stopping service {service}".format(service=service_name)
        win32serviceutil.StopService(serviceName=service_name)

        for top, dirs, nondirs in os.walk(path, followlinks=True):
            for item in nondirs:
                path_to_remove = os.path.join(top, item)
                os.remove(path_to_remove)
                print "file removed: {file}".format(file=path_to_remove)

        print "starting service {service}".format(service=service_name)
        win32serviceutil.StartService(serviceName=service_name)
    else:
        print "current printer spooler in good state, skipped."
        print "[OK] reset printer spooler service finished!"
        sys.exit(0)
else:
    print "Error: {path} not found, system files broken!".format(path=path)
    sys.exit(1)

status_code = win32serviceutil.QueryServiceStatus(service_name)[1]
if status_code == 4 or status_code == 2:
    print "[OK] reset printer spooler service successfully!"
else:
    print status_code
