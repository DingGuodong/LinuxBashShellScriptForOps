#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created by PyCharm.
File Name:              LinuxBashShellScriptForOps:multiprocessing-child-can-interrupt-by-keyboard.py
Version:                0.0.1
Author:                 dgden
Author Email:           dgdenterprise@gmail.com
URL:                    https://github.com/DingGuodong/LinuxBashShellScriptForOps
Download URL:           https://github.com/DingGuodong/LinuxBashShellScriptForOps/tarball/master
Create Date:            2020/4/3
Create Time:            10:34
Description:            multiprocessing child can interrupt by keyboard for python2.x
Long Description:       
References:             
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
import time
from multiprocessing import Pool

import six


def do_a_long_time_task(x):
    print("do a long time task for %d" % x)
    time.sleep(1000)
    return True


if __name__ == '__main__':
    if not six.PY2:
        raise RuntimeError("only python 2.x is supported! ")

    pool = Pool(2)  # 2 CPU cores
    # [Keyboard Interrupts with python's multiprocessing Pool](
    # https://stackoverflow.com/questions/1408356/keyboard-interrupts-with-pythons-multiprocessing-pool)
    # [Python 中 Ctrl+C 不能终止 Multiprocessing Pool 的解决方案](https://segmentfault.com/a/1190000004172444)
    pool.map_async(do_a_long_time_task, range(10)).get(timeout=99999)  # 99999 > 86400(60 * 60 * 24)
