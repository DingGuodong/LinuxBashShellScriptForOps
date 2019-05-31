#!/usr/bin/python
# encoding: utf-8
# -*- coding: utf8 -*-
"""
Created by PyCharm.
File:               LinuxBashShellScriptForOps:truecatchException.py
User:               Guodong
Create Date:        2016/9/20
Create Time:        16:03
 """
import sys

try:
    import os

except SystemExit:
    raise SystemExit

except Exception as e:
    import traceback

    sys.stderr.write("Unhandled exception: %s \n" % str(e))
    sys.stderr.write("traceback: %s" % traceback.format_exc())
    sys.stderr.flush()
    print("Help Link: http://stackoverflow.com/search?q=[python]+" + str(e))
    sys.exit(1)
