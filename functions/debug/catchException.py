#!/usr/bin/python
# encoding: utf-8
# -*- coding: utf8 -*-
"""
Created by PyCharm.
File:               LinuxBashShellScriptForOps:catchException.py
User:               Guodong
Create Date:        2016/8/30
Create Time:        10:36
 """
import sys

try:
    import os

except SystemExit, e:
    raise SystemExit

except Exception, e:
    import traceback

    sys.stderr.write("Unhandled exception: %s" % str(e))
    sys.stderr.write("traceback: %s" % traceback.format_exc())
    sys.exit(1)
