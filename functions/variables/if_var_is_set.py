#!/usr/bin/python
# encoding: utf-8
# -*- coding: utf8 -*-
"""
Created by PyCharm.
File:               LinuxBashShellScriptForOps:if_var_is_set.py
User:               Guodong
Create Date:        2016/9/5
Create Time:        14:02
 """

# if is None?
var = ""  # var is False
if var is None:
    pass

# if is set?
var = ""
if 'var' in dir():
    pass
