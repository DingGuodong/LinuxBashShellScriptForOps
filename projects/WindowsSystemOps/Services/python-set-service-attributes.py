#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created by PyCharm.
File Name:              LinuxBashShellScriptForOps:python-set-service-attributes.py
Version:                0.0.1
Author:                 dgden
Author Email:           dgdenterprise@gmail.com
URL:                    https://github.com/DingGuodong/LinuxBashShellScriptForOps
Download URL:           https://github.com/DingGuodong/LinuxBashShellScriptForOps/tarball/master
Create Date:            2020/1/30
Create Time:            17:17
Description:            
Long Description:       
References:             
Prerequisites:          []
Development Status:     3 - Alpha, 5 - Production/Stable
Environment:            Console
Intended Audience:      System Administrators, Developers, End Users/Desktop
License:                Freeware, Freely Distributable
Natural Language:       English, Chinese (Simplified)
Operating System:       POSIX :: Linux, Microsoft :: Windows
Programming Language:   Python :: 2.6
Programming Language:   Python :: 2.7
Topic:                  Utilities
 """
import sys

import pywintypes
import win32service

try:
    scm = win32service.OpenSCManager(None, None, win32service.SC_MANAGER_ALL_ACCESS)
except pywintypes.error as e:
    for msg in (x.decode('gbk') if isinstance(x, str) else x for x in e):
        print(msg),
    sys.exit(1)
service_handle = win32service.OpenService(scm, 'XLServicePlatform', win32service.SC_MANAGER_ALL_ACCESS)

# https://docs.microsoft.com/en-us/windows/win32/api/winsvc/ns-winsvc-service_status?redirectedfrom=MSDN
dwCurrentState = win32service.QueryServiceStatus(service_handle)[1]

currentServiceConfig = win32service.QueryServiceConfig(service_handle)
# http://timgolden.me.uk/pywin32-docs/win32service__ChangeServiceConfig_meth.html
