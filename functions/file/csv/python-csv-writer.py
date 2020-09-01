#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created by PyCharm.
File Name:              LinuxBashShellScriptForOps:python-csv-writer.py
Version:                0.0.1
Author:                 dgden
Author Email:           dgdenterprise@gmail.com
URL:                    https://github.com/DingGuodong/LinuxBashShellScriptForOps
Download URL:           https://github.com/DingGuodong/LinuxBashShellScriptForOps/tarball/master
Create Date:            2020/9/1
Create Time:            14:06
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
import csv

lines = """Email                  ,Name         ,NewEmail                   ,Status
chris1.ding@example.com,Chris.Ding丁国栋,chris1.ding@new_example.com,0
chris2.ding@example.com,Chris.Ding丁国栋,chris2.ding@new_example.com,0
"""

# note: newline may not work well on Windows
with open("simple.csv", 'w', encoding="utf-8", newline='\n') as fp:
    writer = csv.writer(fp)
    writer.writerows([line.split(",") for line in lines.strip().split("\n")])
