#!/usr/bin/python
# encoding: utf-8
# -*- coding: utf8 -*-
"""
Created by PyCharm.
File Name:              LinuxBashShellScriptForOps:pyWhoisQuery.py
Version:                0.0.1
Author:                 Guodong
Author Email:           dgdenterprise@gmail.com
URL:                    https://github.com/DingGuodong/LinuxBashShellScriptForOps
Download URL:           https://github.com/DingGuodong/LinuxBashShellScriptForOps/tarball/master
Create Date:            2018/4/8
Create Time:            15:57
Description:            python whois query
Long Description:
                        whois.cnnic.net.cn (218.241.97.11)
                        218.241.97.11 M.whois-servers.net
                        218.241.97.11 COM.whois-servers.net
                        218.241.97.11 CN.whois-servers.net
References:             https://pypi.python.org/pypi/whois
                        https://pypi.python.org/pypi/python-whois-extended/0.6.10
Prerequisites:          pip install whois, Linux “whois” command is required
                        pip install python-whois-extended
                        Windows user can install "whois" by sysinternals(https://technet.microsoft.com/en-us/sysinternals/bb842062)
Development Status:     3 - Alpha, 5 - Production/Stable
Environment:            Console
Intended Audience:      System Administrators, Developers, End Users/Desktop
License:                Freeware, Freely Distributable
Natural Language:       English, Chinese (Simplified)
Operating System:       POSIX :: Linux, Microsoft :: Windows
Programming Language:   Python :: 3

Topic:                  Utilities
 """
import socket

socket.setdefaulttimeout(10)

import whois

domain = whois.query('baidu.com')
print(domain.__dict__)
