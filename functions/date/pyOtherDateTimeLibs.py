#!/usr/bin/python
# encoding: utf-8
# -*- coding: utf8 -*-
"""
Created by PyCharm.
File Name:              LinuxBashShellScriptForOps:pyOtherDateTimeLibs.py
Version:                0.0.1
Author:                 Guodong
Author Email:           dgdenterprise@gmail.com
URL:                    https://github.com/DingGuodong/LinuxBashShellScriptForOps
Download URL:           https://github.com/DingGuodong/LinuxBashShellScriptForOps/tarball/master
Create Date:            2017/12/21
Create Time:            11:23
Description:            Arrow - Better dates & times for Python
Long Description:       
References:             https://github.com/crsmithdev/arrow
                        http://arrow.readthedocs.io/en/latest/
                        http://arrow.readthedocs.io/en/latest/#arrow-better-dates-and-times-for-python
Prerequisites:          pip install arrow
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
import arrow

print(arrow.now())
print(arrow.now('Asia/Shanghai'))  # arrow.now('US/Pacific')

print(arrow.get(1513828844).format())

utc = arrow.utcnow()
print(utc)
print(utc.to('local'))

local = utc.to('Asia/Shanghai')
print(local.timestamp)
print(local.format())
print(local.format('YYYY-MM-DD HH:mm:ss ZZ'))  # http://arrow.readthedocs.io/en/latest/#tokens
print(local.humanize())
print(local.shift(hours=2).humanize(locale='zh_cn'))

print(arrow.get('2013-05-11T21:23:58.970460+00:00').format())
