#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created by PyCharm.
File Name:              LinuxBashShellScriptForOps:getMemoryInfo.py
Version:                0.0.1
Author:                 dgden
Author Email:           dgdenterprise@gmail.com
URL:                    https://github.com/DingGuodong/LinuxBashShellScriptForOps
Download URL:           https://github.com/DingGuodong/LinuxBashShellScriptForOps/tarball/master
Create Date:            2019/10/22
Create Time:            13:52
Description:            
Long Description:       
References:             http://man7.org/linux/man-pages/man5/proc.5.html
                        /proc/[pid]/statm
                        /proc/[pid]/status
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

import psutil

process_name = 'python.exe'
for item in psutil.process_iter():
    if item.name() == process_name:
        print(item)
        print(dir(item))
        print(item.memory_info())  # same as 'item.memory_info_ex()'
        print(item.memory_full_info())  # psutil.AccessDenied, Run as Administrator
        print(item.memory_percent())
