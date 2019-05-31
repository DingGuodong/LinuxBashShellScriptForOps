#!/usr/bin/python
# encoding: utf-8
# -*- coding: utf8 -*-
"""
Created by PyCharm.
File:               LinuxBashShellScriptForOps:unicode2gbk.py
User:               Guodong
Create Date:        2016/12/12
Create Time:        9:52
 """
import sys
import importlib

print(str(eval(repr('\xbe\xdc\xbe\xf8\xb7\xc3\xce\xca\xa1\xa3')), 'gbk'))

message = (5, 'OpenSCManager', '\xbe\xdc\xbe\xf8\xb7\xc3\xce\xca\xa1\xa3')
print(str(eval(repr(message[2])), 'gbk'))

print(sys.getdefaultencoding())
print(sys.stdout.encoding)
if 'utf8' not in sys.getdefaultencoding():
    importlib.reload(sys)
    sys.setdefaultencoding("utf8")
    print(sys.getdefaultencoding())
