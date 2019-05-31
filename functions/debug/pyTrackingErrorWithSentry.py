#!/usr/bin/python
# encoding: utf-8
# -*- coding: utf8 -*-
"""
Created by PyCharm.
File Name:              LinuxBashShellScriptForOps:pyServicesManagerBasedOnWMI.py
Version:                0.0.1
Author:                 Guodong
Author Email:           dgdenterprise@gmail.com
URL:                    https://github.com/DingGuodong/LinuxBashShellScriptForOps
Download URL:           https://github.com/DingGuodong/LinuxBashShellScriptForOps/tarball/master
Create Date:            2017/12/4
Create Time:            12:51
Description:            Python error tracking with Sentry, use Sentry to caught exception and trace errors
Long Description:       
References:             https://sentry.io/for/python/
Prerequisites:          pip3 install wmi raven pywin32
Development Status:     3 - Alpha, 5 - Production/Stable
Environment:            Console
Intended Audience:      System Administrators, Developers, End Users/Desktop
License:                Freeware, Freely Distributable
Natural Language:       English, Chinese (Simplified)
Operating System:       POSIX :: Linux, Microsoft :: Windows
Programming Language:   Python :: 3
Topic:                  Utilities
 """

import wmi

from raven import Client

client = Client('http://4f140f7845004be4a5a60bec357a54d3:b97e7d61bcdb434093f905f0f6cbabcc@192.168.88.19:9000/2')

try:

    c = wmi.WMI()

    for service in c.Win32_Service(State="Running"):
        if service.Name.lower() == u"ImControllerService".lower():
            print(service)
            break
    raise RuntimeError("throw a exception on purpose")
except Exception as _:
    del _
    client.captureException()
    # client.captureMessage('Something went fundamentally wrong') # don not use and this is helpless really
