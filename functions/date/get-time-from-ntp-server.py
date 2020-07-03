#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created by PyCharm.
File Name:              LinuxBashShellScriptForOps:get-time-from-ntp-server.py
Version:                0.0.1
Author:                 dgden
Author Email:           dgdenterprise@gmail.com
URL:                    https://github.com/DingGuodong/LinuxBashShellScriptForOps
Download URL:           https://github.com/DingGuodong/LinuxBashShellScriptForOps/tarball/master
Create Date:            2020/7/2
Create Time:            10:52
Description:            get time from ntp server
Long Description:       python -c "import ntplib;from time import ctime;print(ctime(ntplib.NTPClient().request('pool.ntp.org').tx_time))"
References:             
Prerequisites:          sudo -H pip install ntplib
Development Status:     3 - Alpha, 5 - Production/Stable
Environment:            Console
Intended Audience:      System Administrators, Developers, End Users/Desktop
License:                Freeware, Freely Distributable
Natural Language:       English, Chinese (Simplified)
Operating System:       POSIX :: Linux, Microsoft :: Windows
Programming Language:   Python :: 3
Topic:                  Utilities
 """
import time
from time import ctime

import ntplib

c = ntplib.NTPClient()
response = c.request('pool.ntp.org')
print("current offset time: {}".format(response.offset))
print("current server time: {}".format(ctime(response.tx_time)))
print("current system time: {}".format(ctime()))
print("current system time: {}".format(time.strftime("%a %b %d %H:%M:%S %Y")))
