#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created by PyCharm.
File Name:              LinuxBashShellScriptForOps:use-traceback-example-01.py
Version:                0.0.1
Author:                 dgden
Author Email:           dgdenterprise@gmail.com
URL:                    https://github.com/DingGuodong/LinuxBashShellScriptForOps
Download URL:           https://github.com/DingGuodong/LinuxBashShellScriptForOps/tarball/master
Create Date:            2020/4/3
Create Time:            9:21
Description:            traceback child exception in multiprocessing
Long Description:       
References:             [Python: Multiprocessing and Exceptions](https://jichu4n.com/posts/python-multiprocessing-and-exceptions/)
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

import multiprocessing
import sys
import traceback


def some_func(x):
    return 1.0 / x


def f1(x):
    try:
        return 1 / some_func(x)
    except Exception as e:
        sys.stderr.write('Caught exception in worker thread (x = %d):\n' % x)
        sys.stderr.flush()
        # print('Caught exception in worker thread (x = %d):' % x)

        # This prints the type, value, and stack trace of the current exception being handled.
        traceback.print_exc()
        raise e


def f2():
    raise ZeroDivisionError


if __name__ == '__main__':
    pool = multiprocessing.Pool(5)
    print(pool.map(f1, range(5)))
