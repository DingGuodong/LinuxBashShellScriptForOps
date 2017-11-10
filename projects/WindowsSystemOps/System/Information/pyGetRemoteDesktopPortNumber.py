#!/usr/bin/python
# encoding: utf-8
# -*- coding: utf8 -*-
"""
Created by PyCharm.
File Name:              LinuxBashShellScriptForOps:pyGetRemoteDesktopPortNumber.py
Version:                0.0.1
Author:                 Guodong
Author Email:           dgdenterprise@gmail.com
URL:                    https://github.com/DingGuodong/LinuxBashShellScriptForOps
Download URL:           https://github.com/DingGuodong/LinuxBashShellScriptForOps/tarball/master
Create Date:            2017/11/10
Create Time:            17:48
Description:            get remote desktop port number from Windows registry(regedit) using built-in module _winreg
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


def GetRemoteDesktopPortNumber():
    PortNumber = 3389
    reg_key = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE,
                              "System\\CurrentControlSet\\Control\\Terminal Server\\WinStations\\RDP-Tcp")
    if reg_key:
        PortNumber = _winreg.QueryValueEx(reg_key, "PortNumber")[0]
    return PortNumber


if __name__ == '__main__':
    print GetRemoteDesktopPortNumber()
