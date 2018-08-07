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
import chardet
import requests

test_url = 'https://cookpad.com/'

raw_data = requests.get(test_url).content

encoding_detected = chardet.detect(raw_data)

encoding = encoding_detected.get('encoding')

# encode(): unicode --> str, so it can raise UnicodeDecodeError
# decode(): str --> unicode, so it can raise UnicodeEncodeError
decoded_data = raw_data.decode(encoding).encode('utf-8')

print(encoding_detected)
