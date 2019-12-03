#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created by PyCharm.
File Name:              LinuxBashShellScriptForOps:windows-ansi-mbcs-encoding.py
Version:                0.0.1
Author:                 dgden
Author Email:           dgdenterprise@gmail.com
URL:                    https://github.com/DingGuodong/LinuxBashShellScriptForOps
Download URL:           https://github.com/DingGuodong/LinuxBashShellScriptForOps/tarball/master
Create Date:            2019/11/29
Create Time:            17:57
Description:            python ansi mbcs
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
import subprocess

if os.name == 'nt':
    ANSI = 'mbcs'  # note: mbcs != gbk even if current os's language is Simplified Chinese

    proc_obj = subprocess.Popen("ver", shell=True, stdout=subprocess.PIPE,
                                stderr=subprocess.STDOUT)  # Combine stdout and stderr into stdout
    stdout, stderr = proc_obj.communicate()

    print(stdout.decode(ANSI))  # so mbcs is more general than gbk on Microsoft Windows zh-cn
    print(stdout.decode('gbk'))
