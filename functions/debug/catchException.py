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
    # raise SystemExit("raise SystemExit on purpose")
    # raise Exception("raise Exception on purpose")

except SystemExit, e:
    print(e)
    print(e.args)
    print(e.message)
    sys.exit(1)
except Exception, e:
    sys.stderr.write(e.message + "\n")
    sys.exit(1)
else:
    print("no exceptions here, continue")

finally:
    print("always appear here")

print("exit now following 'else' statement")
