#!/usr/bin/python
# encoding: utf-8
# -*- coding: utf8 -*-
"""
Created by PyCharm.
File:               LinuxBashShellScriptForOps:getLinuxDmesg.py
User:               Guodong
Create Date:        2016/10/28
Create Time:        16:15

yum install -y python-devel
python -m pip install -U pip
pip install psutil

 """

# using python to get 'dmesg' messages with full time human readable

import os
import subprocess
import sys
import time

import psutil


def get_human_readable_dmesg():
    # because can NOT get data from /proc, so use 'dmesg' command to get data
    dmesg = subprocess.check_output(['dmesg']).split('\n')  # check_output is not available in Python 2.6
    for line in dmesg:
        try:
            print time.strftime('%Y-%m-%d %H:%M:%S',
                                time.localtime(
                                    (float(psutil.boot_time()) + float(line.split('] ')[0][2:].strip())))), line
            sys.stdout.flush()
        except ValueError:
            print(line)


if __name__ == '__main__':
    # POSIX = os.name == "posix"
    WINDOWS = os.name == "nt"
    if WINDOWS:
        print "WindowsError, Windows is NOT supported!"
        sys.exit(1)
    else:
        try:
            get_human_readable_dmesg()
        except IOError:
            pass
            # TODO(Guodong Ding) fix next desc when using 'python getLinuxDmesg.py | more' with a 'q' interrupt
            # close failed in file object destructor:
            # sys.excepthook is missing
            # lost sys.stderr
            # Fix: print with sys.stdout.flush()
