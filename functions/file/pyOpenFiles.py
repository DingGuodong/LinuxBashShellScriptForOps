#!/usr/bin/python
# encoding: utf-8
# -*- coding: utf-8 -*-
"""
Created by PyCharm.
File Name:              LinuxBashShellScriptForOps:pyOpenFiles.py
Version:                0.0.1
Author:                 Guodong
Author Email:           dgdenterprise@gmail.com
URL:                    https://github.com/DingGuodong/LinuxBashShellScriptForOps
Download URL:           https://github.com/DingGuodong/LinuxBashShellScriptForOps/tarball/master
Create Date:            2018/11/8
Create Time:            11:36
Description:            guess file encoding and get well encoded byte object
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
from codecs import open as copen

if __name__ == '__main__':
    ansi_file = '/tmp/zh_en_mixed_ansi.txt'  # gen file with 'gbk' default system encoding
    utf8_file = '/tmp/zh_en_mixed_utf8.txt'
    unicode_file = '/tmp/zh_en_mixed_unicode.txt'  # Little-endian UTF-16 Unicode text, with CRLF line terminators

    with copen(ansi_file, encoding='gbk') as f:
        print(f.read())

    with open(utf8_file, 'r', encoding='utf-8') as f:
        print(f.read())

    with copen(unicode_file, 'U', encoding="utf-16") as f:
        print(f.read())

    with open(unicode_file, 'r', encoding="utf-16") as f:
        print(f.read())
