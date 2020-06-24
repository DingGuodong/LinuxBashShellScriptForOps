#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created by PyCharm.
File Name:              LinuxBashShellScriptForOps:pexcept-examples.py
Version:                0.0.1
Author:                 dgden
Author Email:           dgdenterprise@gmail.com
URL:                    https://github.com/DingGuodong/LinuxBashShellScriptForOps
Download URL:           https://github.com/DingGuodong/LinuxBashShellScriptForOps/tarball/master
Create Date:            2020/6/23
Create Time:            16:03
Description:            use pexpect to get wanted output and send string
Long Description:       Pexpect allows your script to spawn a child application and
                        control it as if a human were typing commands.
                        Pexpect is in the spirit of Don Libes’ Expect, but Pexpect is pure Python.
References:             [Pexpect version 4.8](https://pexpect.readthedocs.io/en/stable/)
Prerequisites:          sudo -H pip install pexpect
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

import os

import pexpect
import six

log = open("x.txt", 'w')
if six.PY2:
    child = pexpect.spawn('ssh 127.0.0.1')
else:
    child = pexpect.spawn('ssh 127.0.0.1', encoding='utf-8')

child.logfile = log

username = os.getenv('USER')
prompt = '$' if username != 'root' else '#'

# PS1='# ', PS1='$ ', /etc/profile
child.expect(r'^{username}?.*\{prompt}.$'.format(username=username, prompt=prompt), timeout=10)
print(child.before)
child.sendline("ls x.txt")
child.expect(r'^{username}?.*\{prompt}.$'.format(username=username, prompt=prompt), timeout=2)
print(child.before)
child.close()
print(child.exitstatus, child.signalstatus)
os.system('cat x.txt')
