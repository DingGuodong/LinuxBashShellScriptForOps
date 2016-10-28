#!/usr/bin/python
# encoding: utf-8
# -*- coding: utf8 -*-
"""
Created by PyCharm.
File:               LinuxBashShellScriptForOps:getLinuxDmesg.py
User:               Guodong
Create Date:        2016/10/28
Create Time:        16:15
 """

# using python to get 'dmesg' messages with full time human readable

import os
import time
import psutil
import subprocess
import sys


def getDmesg():
    # because can NOT get data from /proc, so use 'dmesg' command to get data
    dmesg = subprocess.check_output(['dmesg']).split('\n')
    for message in dmesg:
        try:
            print time.strftime('%Y-%m-%d %H:%M:%S',
                                time.localtime(
                                    (float(psutil.boot_time()) + float(message.split('] ')[0][2:].strip())))), message
        except ValueError:
            pass


if __name__ == '__main__':
    # POSIX = os.name == "posix"
    WINDOWS = os.name == "nt"
    if WINDOWS:
        print "WindowsError, Windows is NOT supported!"
        sys.exit(1)
    else:
        try:
            getDmesg()
        except IOError:
            pass
            # TODO(Guodong Ding) fix next desc when using 'python getLinuxDmesg.py | more' with a 'q' interrupt
            # close failed in file object destructor:
            # sys.excepthook is missing
            # lost sys.stderr
