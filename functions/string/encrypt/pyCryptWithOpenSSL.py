#!/usr/bin/python
# encoding: utf-8
# -*- coding: utf-8 -*-
"""
Created by PyCharm.
File Name:              LinuxBashShellScriptForOps:pyCryptWithOpenSSL.py
Version:                0.0.1
Author:                 Guodong
Author Email:           dgdenterprise@gmail.com
URL:                    https://github.com/DingGuodong/LinuxBashShellScriptForOps
Download URL:           https://github.com/DingGuodong/LinuxBashShellScriptForOps/tarball/master
Create Date:            2019/1/8
Create Time:            11:02
Description:            encrypt and decrypt with openssl and libsodium library using ctypes
Long Description:       
References:             https://github.com/shadowsocks/shadowsocks/tree/master/shadowsocks
Prerequisites:          pip install shadowsocks
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

from shadowsocks.cryptor import *

if __name__ == '__main__':
    print("it means openssl and libsodium installed if you not see 'AssertionError' exception.")
    test_encrypt_all()
    test_encryptor()
    test_encrypt_all_m()
