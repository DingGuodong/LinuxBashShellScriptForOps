#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created by PyCharm.
File Name:              LinuxBashShellScriptForOps:pbldf2-examples.py
Version:                0.0.1
Author:                 dgden
Author Email:           dgdenterprise@gmail.com
URL:                    https://github.com/DingGuodong/LinuxBashShellScriptForOps
Download URL:           https://github.com/DingGuodong/LinuxBashShellScriptForOps/tarball/master
Create Date:            2020/8/26
Create Time:            10:35
Description:            generate password hash using pbkdf2
Long Description:       
References:             
Prerequisites:          pip install pbkdf2
                        pip install werkzeug
Development Status:     3 - Alpha, 5 - Production/Stable
Environment:            Console
Intended Audience:      System Administrators, Developers, End Users/Desktop
License:                Freeware, Freely Distributable
Natural Language:       English, Chinese (Simplified)
Operating System:       POSIX :: Linux, Microsoft :: Windows
Programming Language:   Python :: 2.6
Programming Language:   Python :: 2.7
Topic:                  Utilities
Notes: Django also use pbkdf2 as hash crypto

 """
import pbkdf2
from werkzeug.security import generate_password_hash, check_password_hash

hashed_password = pbkdf2.crypt(word="plain_password", salt="OzCRyqV4", iterations=12)
print(hashed_password)

hashed_password = generate_password_hash(password="plain_password", method='pbkdf2:sha256', salt_length=8)
print(hashed_password)
is_valid = check_password_hash(password="plain_password", pwhash=hashed_password)
print(is_valid)
