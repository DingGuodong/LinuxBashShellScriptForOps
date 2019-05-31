#!/usr/bin/python
# encoding: utf-8
# -*- coding: utf-8 -*-
"""
Created by PyCharm.
File Name:              LinuxBashShellScriptForOps:py-get-mac-addr-from-ip.py
Version:                0.0.1
Author:                 Guodong
Author Email:           dgdenterprise@gmail.com
URL:                    https://github.com/DingGuodong/LinuxBashShellScriptForOps
Download URL:           https://github.com/DingGuodong/LinuxBashShellScriptForOps/tarball/master
Create Date:            2018/10/23
Create Time:            11:50
Description:            Get MAC addresses of remote hosts and local interfaces
Long Description:       
References:             https://pypi.org/project/getmac/
Prerequisites:          pip install getmac
                        pip install getmac -i https://pypi.org/simple
Development Status:     3 - Alpha, 5 - Production/Stable
Environment:            Console
Intended Audience:      System Administrators, Developers, End Users/Desktop
License:                Freeware, Freely Distributable
Natural Language:       English, Chinese (Simplified)
Operating System:       POSIX :: Linux, Microsoft :: Windows
Programming Language:   Python :: 3
Topic:                  Utilities
 """
from getmac import get_mac_address

ip_mac = get_mac_address(ip="192.168.88.127")

print(ip_mac)
