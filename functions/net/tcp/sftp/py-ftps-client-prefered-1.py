#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created by PyCharm.
File Name:              LinuxBashShellScriptForOps:py-ftps-client-prefered-1.py
Version:                0.0.1
Author:                 dgden
Author Email:           dgdenterprise@gmail.com
URL:                    https://github.com/DingGuodong/LinuxBashShellScriptForOps
Download URL:           https://github.com/DingGuodong/LinuxBashShellScriptForOps/tarball/master
Create Date:            2020/1/7
Create Time:            11:10
Description:            An alternative FTPS client which better than the python standard library(ftplib)
Long Description:       yum install libcurl-devel
References:             [ftps client based on pycurl](https://pypi.org/project/ftps/)
Prerequisites:          pip install ftps
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
import ftps

client = ftps.FTPS(ftps.FTPS('ftp://<user>:<passwd>@<server>'))
client.list()
