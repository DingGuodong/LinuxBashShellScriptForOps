#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created by PyCharm.
File Name:              LinuxBashShellScriptForOps:test-supported-encoding.py
Version:                0.0.1
Author:                 Guodong
Author Email:           dgdenterprise@gmail.com
URL:                    https://github.com/DingGuodong/LinuxBashShellScriptForOps
Download URL:           https://github.com/DingGuodong/LinuxBashShellScriptForOps/tarball/master
Create Date:            2019/5/23
Create Time:            17:04
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
Programming Language:   Python :: 3
Topic:                  Utilities
 """

import encodings
import locale
import time

encoding = locale.getpreferredencoding()
tzname = time.tzname[0].encode("iso-8859-1").decode(encoding)
known_string = time.tzname[0]
print(known_string)
print(tzname)

# Standard Encodings
# https://docs.python.org/3/library/codecs.html#standard-encodings
std_encoding_codecs_list = set(encodings.aliases.aliases.values())

unknown_string = time.strftime("%Z")
print(unknown_string)

codecs_list = list()
for codec1 in std_encoding_codecs_list:
    try:
        if known_string.encode(codec1).decode(encoding) == tzname:
            codecs_list.append(codec1)
    except (UnicodeEncodeError, UnicodeDecodeError, LookupError, AttributeError):
        continue

for codec in codecs_list:
    for key, value in encodings.aliases.aliases.items():
        if value == codec:
            print(key, value)


print("中国标准时间" == ("ÖÐ¹ú±ê×¼Ê±¼ä".encode("latin_1").decode("gbk")))

