#!/usr/bin/python
# encoding: utf-8
# -*- coding: utf8 -*-
"""
Created by PyCharm.
File:               LinuxBashShellScriptForOps:pyRedisOps.py
User:               Guodong
Create Date:        2016/9/7
Create Time:        10:36
 """

import hiredis

reader = hiredis.Reader()
reader.feed("$5\r\nhello\r\n")
print(reader.gets())
reader.feed("*2\r\n$5\r\nhello\r\n")
print(reader.gets())
reader.feed("$5\r\nworld\r\n")
print(reader.gets())
