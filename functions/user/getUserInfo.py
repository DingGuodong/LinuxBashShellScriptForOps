#!/usr/bin/python
# encoding: utf-8
# -*- coding: utf8 -*-
"""
Created by PyCharm.
File:               LinuxBashShellScriptForOps:getUserInfo.py
User:               Guodong
Create Date:        2016/12/14
Create Time:        11:48
 """
import os
import sys

mswindows = (sys.platform == "win32")
linux2 = (sys.platform == "linux2")

if mswindows:
    platform = "Windows"
    user = os.getenv('USERNAME')
elif linux2:
    platform = "Linux"
    user = os.getenv('USER') or os.getenv('LOGNAME')  # set|&grep =root
else:
    platform = ""
    user = None

user_home = os.path.expanduser('~')  # both Windows and Linux is works, 颚化符 (~)

print("current platform: %s" % platform)
print("current user: %s" % user)
print("current user home: %s" % user_home)
