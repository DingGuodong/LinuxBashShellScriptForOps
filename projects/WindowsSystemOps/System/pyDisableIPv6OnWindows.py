#!/usr/bin/python
# encoding: utf-8
# -*- coding: utf8 -*-
"""
Created by PyCharm.
File Name:              LinuxBashShellScriptForOps:pyDisableIPv6OnWindows.py
Version:                0.0.1
Author:                 Guodong
Author Email:           dgdenterprise@gmail.com
URL:                    https://github.com/DingGuodong/LinuxBashShellScriptForOps
Download URL:           https://github.com/DingGuodong/LinuxBashShellScriptForOps/tarball/master
Create Date:            2018/1/29
Create Time:            17:21
Description:            
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
import _winreg  # from (built-in), 'winreg' module used '_winreg' sometime by 'from _winreg import *'
import sys


def try_run(func):
    from functools import wraps

    @wraps(func)
    def try_exec(*args, **kwargs):
        result = None
        try:
            result = func(*args, **kwargs)
        except WindowsError as e:
            print "Try running {func} failed.".format(func=func.func_name),
            if e.args:
                if e.args[0] == 5:
                    print "Access denied. Please try run as root/Administrator."
                else:
                    print e
                    print e.args
                sys.exit(1)
        return result

    return try_exec


def getCurrentIPv6SettingFromRegedit():
    # Windows Server 2012 R2
    reg_key = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE,
                              "SYSTEM\\CurrentControlSet\\Services\\TCPIP6\\Parameters")
    value = None
    if reg_key:
        value = _winreg.QueryValueEx(reg_key, "DisabledComponents")[0]
    return value


if __name__ == '__main__':
    print getCurrentIPv6SettingFromRegedit()
