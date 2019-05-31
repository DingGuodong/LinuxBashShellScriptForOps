#!/usr/bin/python
# encoding: utf-8
# -*- coding: utf-8 -*-
"""
Created by PyCharm.
File Name:              LinuxBashShellScriptForOps:pyStringIO.py
Version:                0.0.1
Author:                 Guodong
Author Email:           dgdenterprise@gmail.com
URL:                    https://github.com/DingGuodong/LinuxBashShellScriptForOps
Download URL:           https://github.com/DingGuodong/LinuxBashShellScriptForOps/tarball/master
Create Date:            2018/7/31
Create Time:            10:59
Description:            
Long Description:       The StringIO and cStringIO modules are gone.
                        Instead, import the io module and use io.StringIO or io.BytesIO for text and data respectively.
References:             https://docs.python.org/3.0/whatsnew/3.0.html
Prerequisites:          []
Development Status:     3 - Alpha, 5 - Production/Stable
Environment:            Console
Intended Audience:      System Administrators, Developers, End Users/Desktop
License:                Freeware, Freely Distributable
Natural Language:       English, Chinese (Simplified)
Operating System:       POSIX :: Linux, Microsoft :: Windows
Programming Language:   Python :: 3
Topic:                  Utilities
 """
from io import StringIO

import csv

csv_file_content = """Email,Name,NewEmail,Status
chris1.ding@example.com,Chris.Ding丁国栋,chris1.ding@new_example.com,0
chris2.ding@example.com,Chris.Ding丁国栋,chris2.ding@new_example.com,0""".strip()

f = StringIO(csv_file_content)  # f.write(csv_file_content)
print(f.getvalue())

csv_reader = csv.reader(f)
for row in csv_reader:
    print(row)
