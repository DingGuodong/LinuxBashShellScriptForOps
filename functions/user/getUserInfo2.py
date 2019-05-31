#!/usr/bin/python
# encoding: utf-8
# -*- coding: utf8 -*-
"""
Created by PyCharm.
File:               LinuxBashShellScriptForOps:getUserIndo2.py
User:               Guodong
Create Date:        2016/12/21
Create Time:        10:10

A compatible impl to get username on Windows or Linux

 """
import os
import psutil
import datetime
import pytz
import sys
import subprocess

mswindows = (sys.platform == "win32")  # learning from 'subprocess' module
linux = (sys.platform == "linux2")

for name in ('LOGNAME', 'USER', 'LNAME', 'USERNAME'):
    user = os.environ.get(name)
    if user:
        print(user)
        break

if linux:
    proc_obj = subprocess.Popen(r'tty', shell=True, stdout=subprocess.PIPE,
                                stderr=subprocess.STDOUT)
    tty = proc_obj.communicate()[0]
else:
    tty = []

for login in psutil.users():
    username, login_tty, login_host, login_time = [suser for suser in login]
    print(username, login_tty, login_host, login_time, end=' ')
    print(datetime.datetime.fromtimestamp(login_time, pytz.timezone('Asia/Shanghai')).strftime(
        '%Y-%m-%d %H:%M:%S %Z%z'), end=' ')
    if login_tty in tty:
        print('**current user**')
