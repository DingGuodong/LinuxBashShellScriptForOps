#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created by PyCharm.
File Name:              LinuxBashShellScriptForOps:create_readme.md_files.py
Version:                0.0.1
Author:                 dgden
Author Email:           dgdenterprise@gmail.com
URL:                    https://github.com/DingGuodong/LinuxBashShellScriptForOps
Download URL:           https://github.com/DingGuodong/LinuxBashShellScriptForOps/tarball/master
Create Date:            2019/12/27
Create Time:            11:14
Description:            create a README.md in each directory
Long Description:       this script snippet can be used for a git repo which new created
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

filename = 'README.md'
work_dir = "."

for top, dirs, nondirs in os.walk(work_dir, followlinks=True):
    for folder in dirs:
        cur_dir = os.path.join(top, folder)
        if not os.path.exists(cur_dir):
            with open(os.path.join(cur_dir, filename), 'w') as fp:
                fp.write("# About\n")
    else:
        cur_dir = top
        if not os.path.exists(os.path.join(cur_dir, filename)):
            with open(os.path.join(cur_dir, filename), 'w') as fp:
                fp.write("# About\n")
