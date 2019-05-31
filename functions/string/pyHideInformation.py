#!/usr/bin/python
# encoding: utf-8
# -*- coding: utf8 -*-
"""
Created by PyCharm.
File Name:              LinuxBashShellScriptForOps:pyHideInformation.py
Version:                0.0.1
Author:                 Guodong
Author Email:           dgdenterprise@gmail.com
URL:                    https://github.com/DingGuodong/LinuxBashShellScriptForOps
Download URL:           https://github.com/DingGuodong/LinuxBashShellScriptForOps/tarball/master
Create Date:            2017/12/27
Create Time:            18:08
Description:            replace string in a pythonic way
Long Description:       str object in Python is iterable and immutable
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

# hide fist word in Chinese Name, also knows as family name(surname), such as "丁国栋" --> "*国栋"
chinese_name = '丁国栋'
print(chinese_name)
# method 1, bad code, not suit all case
print(chinese_name.replace(chinese_name[0], "*", 1))  #
# method 2, is good enough? more better?
print("".join(["*" if i == 0 else chinese_name[i] for i in range(len(chinese_name))]))

# Hidden bank card number， such as '6222083803006763623' --> '62220838030067****3'
card_id = '6222083803006763623'  # this is an example bank card id, please do NOT use it in real world
print(card_id)
# method 1, bad code, not simple enough
print(card_id[:len(card_id) - (4 + 1)] + "*" * 4 + card_id[-1])
# method 2, bad code, not suit all case
print(card_id.replace(card_id[-5:-1], "*" * 4, 1))
# method 3, is good enough? more better?
print("".join(
    ["*" if i in range(-(1 + 4) + len(card_id), -1 + len(card_id)) else card_id[i] for i in range(len(card_id))]))
