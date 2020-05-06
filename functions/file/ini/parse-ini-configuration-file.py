#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created by PyCharm.
File Name:              LinuxBashShellScriptForOps:parse-ini-configuration-file.py
Version:                0.0.1
Author:                 dgden
Author Email:           dgdenterprise@gmail.com
URL:                    https://github.com/DingGuodong/LinuxBashShellScriptForOps
Download URL:           https://github.com/DingGuodong/LinuxBashShellScriptForOps/tarball/master
Create Date:            2020/4/28
Create Time:            11:09
Description:            python parse .ini, .cnf, .conf file
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
import configparser
config = configparser.ConfigParser(allow_no_value=True, comment_prefixes=";")

config.read("php.ini", encoding='utf-8')

try:
    print(config.get("PHP", "max_execution_time"))
except configparser.NoSectionError as e:
    print("Note: Section is case sensitive")
    raise e

# WARNING: this operation will remove comments in the file
with open("php.ini", 'wb') as fp:
    config.set("PHP", "max_execution_time", value="300")
    config.write(fp)

