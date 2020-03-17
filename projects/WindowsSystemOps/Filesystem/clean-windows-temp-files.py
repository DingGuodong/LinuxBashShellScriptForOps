#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created by PyCharm.
File Name:              LinuxBashShellScriptForOps:clean-windows-temp-files.py
Version:                0.0.1
Author:                 dgden
Author Email:           dgdenterprise@gmail.com
URL:                    https://github.com/DingGuodong/LinuxBashShellScriptForOps
Download URL:           https://github.com/DingGuodong/LinuxBashShellScriptForOps/tarball/master
Create Date:            2020/3/17
Create Time:            11:47
Description:            clean Windows TEMP directory to save disk space
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

TEMP_DIRECTORIES_LIST = [
    r'%SystemRoot%\Temp',  # system TEMP directory
    r'%LOCALAPPDATA%\Temp'  # user TEMP directory
]

for temp_directory in TEMP_DIRECTORIES_LIST:
    temp_directory = os.path.expandvars(temp_directory)
    if os.path.exists(temp_directory):
        print(temp_directory)
        for top, dirs, nondirs in os.walk(temp_directory, followlinks=True):
            for item in nondirs:
                cur_file = os.path.join(top, item)
                try:
                    os.remove(cur_file)
                except WindowsError as e:
                    print(cur_file, e)
                    continue
            for item in dirs:
                cur_dir = cur_file = os.path.join(top, item)
                try:
                    os.removedirs(cur_dir)
                except WindowsError as e:
                    print(cur_file, e)
                    continue

