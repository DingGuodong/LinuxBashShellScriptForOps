#!/usr/bin/python
# encoding: utf-8
# -*- coding: utf8 -*-
"""
Created by PyCharm.
File Name:              LinuxBashShellScriptForOps:pyTestWebPerformance.py
Version:                0.0.1
Author:                 Guodong
Author Email:           dgdenterprise@gmail.com
URL:                    https://github.com/DingGuodong/LinuxBashShellScriptForOps
Download URL:           https://github.com/DingGuodong/LinuxBashShellScriptForOps/tarball/master
Create Date:            2018/3/13
Create Time:            15:36
Description:            python test web performance like Apache ab
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
from StringIO import StringIO

import certifi
import pycurl

data_buffer = StringIO()
URL = "https://github.com"
c = pycurl.Curl()
c.setopt(pycurl.URL, URL)
c.setopt(pycurl.WRITEDATA, data_buffer)
c.setopt(pycurl.FOLLOWLOCATION, 1L)
c.setopt(pycurl.CAINFO, certifi.where())  # c.setopt(pycurl.SSL_VERIFYPEER, False)  # useful for HTTPS connection

try:
    c.perform()
except Exception, e:
    print("connection error:" + str(e))
    c.close()
    sys.exit()

NAMELOOKUP_TIME = c.getinfo(pycurl.NAMELOOKUP_TIME)
CONNECT_TIME = c.getinfo(pycurl.CONNECT_TIME)
PRETRANSFER_TIME = c.getinfo(pycurl.PRETRANSFER_TIME)
STARTTRANSFER_TIME = c.getinfo(pycurl.STARTTRANSFER_TIME)
TOTAL_TIME = c.getinfo(pycurl.TOTAL_TIME)
HTTP_CODE = c.getinfo(pycurl.HTTP_CODE)
SIZE_DOWNLOAD = c.getinfo(pycurl.SIZE_DOWNLOAD)
HEADER_SIZE = c.getinfo(pycurl.HEADER_SIZE)
SPEED_DOWNLOAD = c.getinfo(pycurl.SPEED_DOWNLOAD)
DATA = data_buffer.getvalue()
c.close()

print(u"HTTP状态码：%s" % HTTP_CODE)
print(u"DNS解析时间：%.2f ms" % (NAMELOOKUP_TIME * 1000))
print(u"建立连接时间：%.2f ms" % (CONNECT_TIME * 1000))
print(u"准备传输时间：%.2f ms" % (PRETRANSFER_TIME * 1000))
print(u"传输开始时间：%.2f ms" % (STARTTRANSFER_TIME * 1000))
print(u"传输结束总时间：%.2f ms" % (TOTAL_TIME * 1000))

print(u"下载数据包大小：%d bytes/s" % SIZE_DOWNLOAD)
print(u"HTTP头部大小：%d byte" % HEADER_SIZE)
print(u"平均下载速度：%d bytes/s" % SPEED_DOWNLOAD)
