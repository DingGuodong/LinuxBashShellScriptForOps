#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created by PyCharm.
File Name:              LinuxBashShellScriptForOps:sched-quick-start.py
Version:                0.0.1
Author:                 Guodong
Author Email:           dgdenterprise@gmail.com
URL:                    https://github.com/DingGuodong/LinuxBashShellScriptForOps
Download URL:           https://github.com/DingGuodong/LinuxBashShellScriptForOps/tarball/master
Create Date:            2019/5/20
Create Time:            11:50
Description:            
Long Description:       
References:             https://docs.python.org/2/library/sched.html
Prerequisites:          []
Development Status:     3 - Alpha, 5 - Production/Stable
Environment:            Console
Intended Audience:      System Administrators, Developers, End Users/Desktop
License:                Freeware, Freely Distributable
Natural Language:       English, Chinese (Simplified)
Operating System:       POSIX :: Linux, Microsoft :: Windows
Programming Language:   Python :: 2.6
Programming Language:   Python :: 2.7
Topic:                  Utilities
 """
import sched
import time
from threading import Timer

s = sched.scheduler(time.time, time.sleep)


def print_time():
    print "From print_time", time.time()


def print_some_times():
    print time.time()
    s.enter(5, 1, print_time, ())
    s.enter(10, 1, print_time, ())
    s.run()
    print time.time()


def print_some_times_ts():  # thread-safe
    print time.time()
    Timer(5.0, print_time, []).start()
    Timer(10.0, print_time, []).start()
    time.sleep(11)  # sleep while time-delay events execute
    print time.time()


if __name__ == '__main__':
    print_some_times_ts()
