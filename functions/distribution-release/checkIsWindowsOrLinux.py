#!/usr/bin/python
# encoding: utf-8
# -*- coding: utf8 -*-
"""
Created by PyCharm.
File:               LinuxBashShellScriptForOps:getIfIsWindowsOrLinux.py
User:               Guodong
Create Date:        2016/12/1
Create Time:        10:23
 """
import os
import sys

# https://github.com/giampaolo/psutil/blob/master/psutil/_common.py
POSIX = os.name == "posix"
WINDOWS = os.name == "nt"
LINUX = sys.platform.startswith("linux")
MACOS = sys.platform.startswith("darwin")
OSX = MACOS  # deprecated alias
FREEBSD = sys.platform.startswith("freebsd")
OPENBSD = sys.platform.startswith("openbsd")
NETBSD = sys.platform.startswith("netbsd")
BSD = FREEBSD or OPENBSD or NETBSD
SUNOS = sys.platform.startswith(("sunos", "solaris"))
AIX = sys.platform.startswith("aix")

mswindows = (sys.platform == "win32")  # learning from 'subprocess' module


# linux = (sys.platform == "linux2")

def win_or_linux():
    # os.name ->(sames to) sys.builtin_module_names
    if 'posix' in sys.builtin_module_names:
        os_type = 'Linux'
    elif 'nt' in sys.builtin_module_names:
        os_type = 'Windows'
    else:
        return "others"
    return os_type


def is_windows():
    if "windows" in win_or_linux().lower():
        return True
    else:
        return False


def is_linux():
    if "linux" in win_or_linux().lower():
        return True
    else:
        return False


def is_windows_u2():
    return True if 'nt' in sys.builtin_module_names else False


def is_linux_u2():
    # Note: not validate on Mac OS X
    return True if 'posix' in sys.builtin_module_names else False
