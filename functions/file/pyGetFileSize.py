#!/usr/bin/python
# encoding: utf-8
# -*- coding: utf8 -*-
"""
Created by PyCharm.
File Name:              LinuxBashShellScriptForOps:pyGetFileSize.py
Version:                0.0.1
Author:                 Guodong
Author Email:           dgdenterprise@gmail.com
URL:                    https://github.com/DingGuodong/LinuxBashShellScriptForOps
Download URL:           https://github.com/DingGuodong/LinuxBashShellScriptForOps/tarball/master
Create Date:            2017/11/24
Create Time:            10:09
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
import os

path = 'C:\Users\Guodong\PycharmProjects\LinuxBashShellScriptForOps\projects\LinuxSystemOps'

if os.path.isdir(path):
    size = 0L
    for top, dirs, nondirs in os.walk(path):
        for filename in nondirs:
            full_path = os.path.join(top, filename)
            size += os.path.getsize(full_path)
    print size

print os.stat(__file__).st_size  # equal to: fd = os.open(__file__, os.O_RDONLY);print os.lseek(fd, 0, os.SEEK_END)
print os.path.getsize(__file__)  # equal to: fd = os.open(__file__, os.O_RDONLY);print os.lseek(fd, 0, os.SEEK_END)

# get file on disk usage maybe require system call 'du' command
