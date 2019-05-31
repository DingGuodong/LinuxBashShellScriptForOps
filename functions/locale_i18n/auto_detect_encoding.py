#!/usr/bin/python
# encoding: utf-8
# -*- coding: utf-8 -*-
"""
Created by PyCharm.
File Name:              LinuxBashShellScriptForOps:auto_detect_encoding.py
Version:                0.0.1
Author:                 Guodong
Author Email:           dgdenterprise@gmail.com
URL:                    https://github.com/DingGuodong/LinuxBashShellScriptForOps
Download URL:           https://github.com/DingGuodong/LinuxBashShellScriptForOps/tarball/master
Create Date:            2018/5/28
Create Time:            15:33
Description:            Detect the encoding of the given byte string.
Long Description:       guess encoding
                        Note: some wrong database data types maybe cause unreadable code, see also 'varchar vs nvarchar'
References:             
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
import chardet
import requests
import locale


print(locale.getpreferredencoding())
print(locale.getpreferredencoding(False))
print(locale.getdefaultlocale())

test_url = 'https://cookpad.com/'

response = requests.get(test_url)
content = response.content
text = response.text
print(type(content))
print(type(text))

encoding_detected = chardet.detect(content)

encoding = encoding_detected.get('encoding')

print(encoding_detected)

