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

for name in ('LOGNAME', 'USER', 'LNAME', 'USERNAME'):
    user = os.environ.get(name)
    if user:
        print user
