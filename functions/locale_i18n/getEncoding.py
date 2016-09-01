#!/usr/bin/python
# encoding: utf-8
# -*- coding: utf8 -*-
"""
Created by PyCharm.
File:               LinuxBashShellScriptForOps:__init__.py.py
User:               Guodong
Create Date:        2016/9/1
Create Time:        9:02
 """
import sys

system_encoding = sys.getfilesystemencoding()
print "Current system encoding is \"%s\"." % system_encoding

default_encoding = sys.getdefaultencoding()
print "Default encoding is \"%s\"." % default_encoding

print "".decode(system_encoding).encode("utf-8")
