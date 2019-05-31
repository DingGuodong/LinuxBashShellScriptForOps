#!/usr/bin/python
# encoding: utf-8
# -*- coding: utf8 -*-
"""
Created by PyCharm.
File Name:              LinuxBashShellScriptForOps:pyTimezoneConverter.py
Version:                0.0.1
Author:                 Guodong
Author Email:           dgdenterprise@gmail.com
URL:                    https://github.com/DingGuodong/LinuxBashShellScriptForOps
Download URL:           https://github.com/DingGuodong/LinuxBashShellScriptForOps/tarball/master
Create Date:            2018/6/7
Create Time:            19:00
Description:            timezone converter for datetime object, datetime对象时区转换（方法）
Long Description:       
References:             https://blog.csdn.net/cenziboy/article/details/40348269
Prerequisites:          []
Development Status:     3 - Alpha, 5 - Production/Stable
Environment:            Console
Intended Audience:      System Administrators, Developers, End Users/Desktop
License:                Freeware, Freely Distributable
Natural Language:       English, Chinese (Simplified)
Operating System:       POSIX :: Linux, Microsoft :: Windows
Programming Language:   Python :: 3
Topic:                  Utilities
 """
from datetime import datetime

import tzlocal
from pytz import timezone
from pytz import utc

cst_tz = timezone('Asia/Shanghai')
utc_tz = timezone('UTC')

now = datetime.now().replace(tzinfo=cst_tz)  # specify timezone
utctime = now.astimezone(utc)  # convert timezone here
print ("china now: %s" % now)
print ("utc now: %s" % utctime)

utc_now = datetime.utcnow().replace(tzinfo=utc_tz)  # specify timezone
china_now = utc_now.astimezone(cst_tz)  # convert timezone here
print("utc now: %s" % utc_now)
print("china now: %s" % china_now)

print("format time with a format: %s" % china_now.strftime('%Y-%m-%d %H:%M:%S'))

# UTC time('Z' letter in string) convert to another timezone
print(datetime.strptime('2018-06-07T10:57:14Z', "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone('UTC')).astimezone(
    timezone('Asia/Shanghai'))).strftime('%Y-%m-%d %H:%M:%S')

# figure out local timezone
# https://stackoverflow.com/questions/2720319/python-figure-out-local-timezone
current_timezone = tzlocal.get_localzone().zone
print(current_timezone)

# compare datetime object
expiration = '2018-06-07T10:57:14Z'  # iso format(ISO 8601 format) in UTC
utc_now = datetime.now().replace(tzinfo=timezone('UTC'))
expiration_datetime = datetime.strptime(expiration, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone('UTC'))
print(utc_now < expiration_datetime)
