#!/usr/bin/python
# encoding: utf-8
# -*- coding: utf8 -*-
"""
Created by PyCharm.
File:               LinuxBashShellScriptForOps:getSystemVersion.py
User:               Guodong
Create Date:        2016/12/16
Create Time:        14:51
 """
import sys
import os
import platform
import subprocess
import codecs
import locale


def get_system_encoding():
    """
    The encoding of the default system locale but falls back to the given
    fallback encoding if the encoding is unsupported by python or could
    not be determined.  See tickets #10335 and #5846
    """
    try:
        encoding = locale.getdefaultlocale()[1] or 'ascii'
        codecs.lookup(encoding)
    except Exception:
        encoding = 'ascii'
    return encoding


DEFAULT_LOCALE_ENCODING = get_system_encoding()

mswindows = (sys.platform == "win32")  # learning from 'subprocess' module
linux = (sys.platform == "linux2")

hidden_hostname = True

if mswindows:
    uname = list(platform.uname())
    if hidden_hostname:
        uname[1] = "hidden_hostname"
    print uname

    import _winreg

    try:
        reg_key = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE, "SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion")
        if reg_key:
            ProductName = _winreg.QueryValueEx(reg_key, "ProductName")[0] or None
            EditionId = _winreg.QueryValueEx(reg_key, "EditionId")[0] or None
            ReleaseId = _winreg.QueryValueEx(reg_key, "ReleaseId")[0] or None
            CurrentBuild = _winreg.QueryValueEx(reg_key, "CurrentBuild")[0] or None
            BuildLabEx = _winreg.QueryValueEx(reg_key, "BuildLabEx")[0][:9] or None
            print (ProductName, EditionId, ReleaseId, CurrentBuild, BuildLabEx)
    except Exception as e:
        print e.message.decode(DEFAULT_LOCALE_ENCODING)

if linux:
    uname = list(platform.uname())
    if hidden_hostname:
        uname[1] = "hidden_hostname"
    print uname

    proc_obj = subprocess.Popen(r'uname -a', shell=True, stdout=subprocess.PIPE,
                                stderr=subprocess.STDOUT)
    result = proc_obj.stdout.read().strip().decode(DEFAULT_LOCALE_ENCODING)
    if result:
        print result

    if os.path.isfile("/proc/version"):
        with open("/proc/version", 'r') as f:
            content = f.read().strip()
        if content != "":
            print content

    if os.path.isfile("/etc/issue"):
        with open("/etc/issue", 'r') as f:
            content = f.read().strip()
        if content != "":
            print content
