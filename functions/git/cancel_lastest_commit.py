#!/usr/bin/python
# encoding: utf-8
"""
Created by PyCharm.
File Name:              LinuxBashShellScriptForOps:cancel_lastest_commit.py
Version:                0.0.1
Author:                 Guodong
Author Email:           dgdenterprise@gmail.com
URL:                    https://github.com/DingGuodong/LinuxBashShellScriptForOps
Download URL:           https://github.com/DingGuodong/LinuxBashShellScriptForOps/tarball/master
Create Date:            2018/3/5
Create Time:            17:24
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
os.chdir('C:\\Users\\dgden\\PycharmProjects\\LinuxBashShellScriptForOps')
os.system("git reset HEAD^ --soft")
