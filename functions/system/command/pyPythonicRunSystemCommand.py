#!/usr/bin/python
# encoding: utf-8
# -*- coding: utf8 -*-
"""
Created by PyCharm.
File Name:              LinuxBashShellScriptForOps:pyPythonicRunSystemCommand.py
Version:                0.0.1
Author:                 Guodong
Author Email:           dgdenterprise@gmail.com
URL:                    https://github.com/DingGuodong/LinuxBashShellScriptForOps
Download URL:           https://github.com/DingGuodong/LinuxBashShellScriptForOps/tarball/master
Create Date:            2018/1/24
Create Time:            15:43
Description:            simple and pythonic system command executor
Long Description:       
References:             https://github.com/ajenti/ajenti/blob/1.x/ajenti/api/helpers.py
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
import subprocess

import gevent


def subprocess_call_background(*args, **kwargs):
    p = subprocess.Popen(*args, **kwargs)
    gevent.sleep(0)
    return p.wait()


def subprocess_check_output_background(*args, **kwargs):
    p = subprocess.Popen(*args, stdout=subprocess.PIPE, **kwargs)
    gevent.sleep(0)
    return p.communicate()[0]


if __name__ == '__main__':
    # simple usage example
    subprocess_call_background(["/etc/init.d/nginx", "start"])

    for line in subprocess_check_output_background(['chkconfig', '--list']).splitlines():
        print line

    for line in subprocess_check_output_background(['service', '--status-all']).splitlines():
        print line

    subprocess_call_background(["ls", "-al"])

    for line in subprocess_check_output_background(['ls', '-al']).splitlines():
        print line
