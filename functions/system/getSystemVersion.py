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
import codecs
import locale
import os
import platform
import socket
import subprocess
import sys
import time


def get_system_encoding():
    """
    The encoding of the default system locale but falls back to the given
    fallback encoding if the encoding is unsupported by python or could
    not be determined.  See tickets #10335 and #5846
    """
    try:
        encoding = locale.getdefaultlocale()[1] or 'ascii'
        codecs.lookup(encoding)
    except Exception as _:
        del _
        encoding = 'ascii'
    return encoding


DEFAULT_LOCALE_ENCODING = get_system_encoding()

mswindows = (sys.platform == "win32")  # learning from 'subprocess' module
linux = (sys.platform == "linux2")

print(platform.node() or socket.gethostname())
print(platform.uname())

if mswindows:
    import _winreg
    try:
        reg_key = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE, "SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion")
        if reg_key:
            InstallationType = _winreg.QueryValueEx(reg_key, "InstallationType")[0] or ""
            if InstallationType and InstallationType == 'Client':
                InstallDate = time.strftime('%Y-%m-%d %H:%M:%S',
                                            time.localtime(_winreg.QueryValueEx(reg_key, "InstallDate")[0]))
                ProductName = _winreg.QueryValueEx(reg_key, "ProductName")[0] or None
                EditionId = _winreg.QueryValueEx(reg_key, "EditionId")[0] or None
                ReleaseId = _winreg.QueryValueEx(reg_key, "ReleaseId")[0] or None
                CurrentBuild = _winreg.QueryValueEx(reg_key, "CurrentBuild")[0] or None
                CurrentVersion = _winreg.QueryValueEx(reg_key, "CurrentVersion")[0] or None
                BuildLabEx = _winreg.QueryValueEx(reg_key, "BuildLabEx")[0][:9] or None
                ProductId = _winreg.QueryValueEx(reg_key, "ProductId")[0] or None
                UBR = _winreg.QueryValueEx(reg_key, "UBR")[0] or None
                print(
                    InstallDate, ProductName, EditionId, ReleaseId, CurrentVersion, CurrentBuild, BuildLabEx, ProductId,
                    UBR)
                print(ProductName, ReleaseId, InstallDate, CurrentBuild, UBR)
            elif InstallationType and InstallationType == 'Server':
                InstallDate = time.strftime('%Y-%m-%d %H:%M:%S',
                                            time.localtime(_winreg.QueryValueEx(reg_key, "InstallDate")[0]))
                ProductName = _winreg.QueryValueEx(reg_key, "ProductName")[0] or None
                EditionId = _winreg.QueryValueEx(reg_key, "EditionId")[0] or None
                CurrentVersion = _winreg.QueryValueEx(reg_key, "CurrentVersion")[0] or None
                CurrentBuild = _winreg.QueryValueEx(reg_key, "CurrentBuild")[0] or None
                BuildLabEx = _winreg.QueryValueEx(reg_key, "BuildLabEx")[0][:9] or None
                if CurrentVersion <= '6.1':  # 6.1 include 'Windows Server 2008 R2(6.1)'
                    print(InstallDate, ProductName, EditionId, CurrentVersion, CurrentBuild, BuildLabEx)
                else:
                    ProductId = _winreg.QueryValueEx(reg_key, "ProductId")[
                                    0] or None  # Windows Server 2008 R2 is not supported
                    print(InstallDate, ProductName, EditionId, CurrentVersion, CurrentBuild, BuildLabEx, ProductId)
        reg_key_machine_id = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\SQMClient")
        if reg_key_machine_id:
            MachineId = _winreg.QueryValueEx(reg_key_machine_id, "MachineId")[0] or None
            print(MachineId)

    except WindowsError as e:
        print 'WindowsError is captured.'
        print e
        print e.args
        print e.message.decode(DEFAULT_LOCALE_ENCODING)
    except Exception as e:
        print e
        print e.args
        print e.message.decode(DEFAULT_LOCALE_ENCODING)

if linux:
    proc_obj = subprocess.Popen(r'lsb_release -idrc', shell=True, stdout=subprocess.PIPE,
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
