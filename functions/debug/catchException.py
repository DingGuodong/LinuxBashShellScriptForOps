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

import time

try:
    import os
    # raise SystemExit("raise SystemExit on purpose")
    # raise Exception("raise Exception on purpose")

except SystemExit as e:
    print(e)
    time.sleep(10)  # kill process here, finally statement will skipped
    print(e.args)
    sys.exit(1)
except Exception as e:
    sys.stderr.write(e.__str__())
    sys.exit(1)
else:
    print("no exceptions here, continue")

finally:
    print("always appear here")

print("exit now following 'else' statement")
