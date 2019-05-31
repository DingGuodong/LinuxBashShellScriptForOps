#!/usr/bin/python
# encoding: utf-8
# -*- coding: utf8 -*-
"""
Created by PyCharm.
File Name:              LinuxBashShellScriptForOps:pyRemoteDesktopOps.py
Version:                0.0.1
Author:                 Guodong
Author Email:           dgdenterprise@gmail.com
URL:                    https://github.com/DingGuodong/LinuxBashShellScriptForOps
Download URL:           https://github.com/DingGuodong/LinuxBashShellScriptForOps/tarball/master
Create Date:            2017/11/10
Create Time:            17:48
Description:            some remote desktop ops from Windows registry('regedit') using built-in module _winreg
Long Description:       
References:             
Prerequisites:          []
Development Status:     3 - Alpha, 5 - Production/Stable
Environment:            Console
Intended Audience:      System Administrators, Developers, End Users/Desktop
License:                Freeware, Freely Distributable
Natural Language:       English, Chinese (Simplified)
Operating System:       Microsoft :: Windows
Programming Language:   Python :: 3

Topic:                  Utilities
 """
import sys
import winreg  # from (built-in), 'winreg' module used '_winreg' sometime by 'from _winreg import *'


def try_run(func):
    from functools import wraps

    @wraps(func)
    def try_exec(*args, **kwargs):
        result = None
        try:
            result = func(*args, **kwargs)
        except WindowsError as e:
            print("Try running {func} failed.".format(func=func.__name__), end=' ')
            if e.args:
                if e.args[0] == 5:
                    print("Access denied. Please try run as root/Administrator.")
                else:
                    print(e)
                    print(e.args)
                sys.exit(1)
        return result

    return try_exec


def getRemoteDesktopPortNumber():
    PortNumber = 3389
    reg_key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,
                             "System\\CurrentControlSet\\Control\\Terminal Server\\WinStations\\RDP-Tcp")
    if reg_key:
        PortNumber = winreg.QueryValueEx(reg_key, "PortNumber")[0]  # [0] is value, [1] is type(such as REG_DWORD == 4)
    return PortNumber


@try_run
def setRemoteDesktopPortNumber(port):
    port_wanted = '9833'
    if isinstance(port, int):
        if port != 3389:
            port_wanted = str(port)
    if isinstance(port, str):
        if port != '3389':
            port_wanted = str(port)
    if isinstance(port, str):
        if port != '3389':
            port_wanted = port

    reg_key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,
                             "System\\CurrentControlSet\\Control\\Terminal Server\\WinStations\\RDP-Tcp")
    if reg_key:
        winreg.SetValue(reg_key, "PortNumber", winreg.REG_SZ, port_wanted)
        print("current remote desktop port number is {port}".format(port=port_wanted))


def getRemoteDesktopStatus():
    reg_key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,
                             "System\\CurrentControlSet\\Control\\Terminal Server")
    if reg_key:
        value = winreg.QueryValueEx(reg_key, "fDenyTSConnections")[0]
        if value == 1:
            return False
        elif value == 0:
            return True
        else:
            print("if go to this line means 'RDP rules' changed")
            print(value)
            return False


@try_run
def changeRemoteDesktopSetting(enableRDP=True):
    reg_key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,
                             "System\\CurrentControlSet\\Control\\Terminal Server")
    if reg_key:
        if enableRDP:
            winreg.SetValue(reg_key, "fDenyTSConnections", winreg.REG_SZ, '0')
        else:
            winreg.SetValue(reg_key, "fDenyTSConnections", winreg.REG_SZ, '1')


def enableRemoteDesktop():
    changeRemoteDesktopSetting(enableRDP=True)
    print("remote desktop service is now enabled with port {port}".format(port=getRemoteDesktopPortNumber()))


def disableRemoteDesktop():
    changeRemoteDesktopSetting(enableRDP=False)
    print("remote desktop service is now disabled.")


if __name__ == '__main__':
    if not getRemoteDesktopStatus():
        setRemoteDesktopPortNumber(6987)
        enableRemoteDesktop()
