#!/usr/bin/python
# encoding: utf-8
# -*- coding: utf8 -*-
"""
Created by PyCharm.
File:               LinuxBashShellScriptForOps:mkdirOnWindows.py
User:               Guodong
Create Date:        2016/12/7
Create Time:        10:01
 """
import os

HOME = os.path.expanduser('~')  # both Windows and Linux is works
name = ".pip"
path = os.path.join(HOME, name)
if not os.path.isdir(path):
    os.makedirs(path)
    if os.path.isdir(path):
        print "Done"
else:
    print "%s: cannot create directory '%s' : File exists" % (os.path.basename(__file__), path)

data = r"""[global]
index-url = https://mirrors.ustc.edu.cn/pypi/web/simple
format = columns"""
pip_conf = os.path.join(path, "pip.conf")

with open(pip_conf, 'w') as f:
    f.write(data)
    f.flush()

if os.access(pip_conf, os.F_OK) and os.access(pip_conf, os.R_OK):
    # print "%s: '%s' is writen successfully." % (os.path.basename(__file__), pip_conf)
    print "'%s' is writen successfully." % pip_conf
