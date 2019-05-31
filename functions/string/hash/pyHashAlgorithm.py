#!/usr/bin/python
# encoding: utf-8
# -*- coding: utf8 -*-
"""
Created by PyCharm.
File Name:              LinuxBashShellScriptForOps:pyHashAlgorithm.py
Version:                0.0.1
Author:                 Guodong
Author Email:           dgdenterprise@gmail.com
URL:                    https://github.com/DingGuodong/LinuxBashShellScriptForOps
Download URL:           https://github.com/DingGuodong/LinuxBashShellScriptForOps/tarball/master
Create Date:            2018/5/16
Create Time:            20:19
Description:            hash algorithm exampleshash algorithm examples
Long Description:       
References:             see also 'django.utils.crypto'
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
import base64
import hashlib
import hmac


def hmac_md5(key, msg):
    return hmac.new(key, msg, digestmod=hashlib.md5).hexdigest()


if __name__ == '__main__':
    print((hmac_md5('Hello, world!'.encode('utf-8'), 'secret')))
    print((hmac_md5('Hello, world!', 'secret')))
    print((base64.b64encode('37a169bbacb03ca1c4b855bb69ac3836')))
