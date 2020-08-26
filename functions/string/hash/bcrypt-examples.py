#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created by PyCharm.
File Name:              LinuxBashShellScriptForOps:bcrypt-examples.py
Version:                0.0.1
Author:                 dgden
Author Email:           dgdenterprise@gmail.com
URL:                    https://github.com/DingGuodong/LinuxBashShellScriptForOps
Download URL:           https://github.com/DingGuodong/LinuxBashShellScriptForOps/tarball/master
Create Date:            2020/8/26
Create Time:            10:12
Description:            hash password using bcrypt
Long Description:       
References:             
Prerequisites:          pip install bcrypt
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

import bcrypt

salt = bcrypt.gensalt(rounds=12, prefix='2b')
print(salt)

# recommended password length is between 0 and 72
plain_password = 'plain_password'

hashed_password = bcrypt.hashpw(password=plain_password, salt=salt)
print(hashed_password)

is_valid = bcrypt.checkpw(password=plain_password, hashed_password=hashed_password)
print(is_valid)
