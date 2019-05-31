#!/usr/bin/python
# encoding: utf-8
# -*- coding: utf8 -*-
"""
Created by PyCharm.
File:               LinuxBashShellScriptForOps:pyReportProcess.py
User:               Guodong
Create Date:        2016/11/16
Create Time:        17:15
 """
import psutil

flag = True

while flag:
    print('''Input: pid or name (Enter at least one)
Output: process object, ppid, name of ppid
''')
    pid = input("Please input the Process Pid:")
    name = input('Please input the Process Name:')
    if pid != '' or name != '':
        flag = False

not_exist = True

for obj in psutil.process_iter():
    # print obj.__dict__.items()
    if str(obj.pid) == pid or obj.name() == name:
        print(obj, obj.ppid(), [x.name() for x in psutil.process_iter() if x.pid == obj.ppid()])
        not_exist = False
if not_exist:
    print('Process Pid:%s or Name:%s is NOT Found!' % ((pid or '-'), (name or '-')))
