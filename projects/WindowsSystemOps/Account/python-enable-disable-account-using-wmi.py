#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created by PyCharm.
File Name:              LinuxBashShellScriptForOps:python-enable-disable-account-using-wmi.py
Version:                0.0.1
Author:                 dgden
Author Email:           dgdenterprise@gmail.com
URL:                    https://github.com/DingGuodong/LinuxBashShellScriptForOps
Download URL:           https://github.com/DingGuodong/LinuxBashShellScriptForOps/tarball/master
Create Date:            2020/10/15
Create Time:            16:37
Description:            enable or disable account using pywin32
Long Description:       
References:             
Prerequisites:          pip install pywin32
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
import sys

import pywintypes
import win32net
import win32netcon
import wmi

user_info_global = {}


def _get_account_info(name):
    conn = wmi.WMI()
    user_obj = conn.Win32_UserAccount(Name=name)[0]
    return user_obj


def _enable_account(name):
    conn = wmi.WMI()
    user_obj = conn.Win32_UserAccount(Name=name)[0]
    user_obj.Disabled = False
    user_obj.put()  # Running with Administrator Privileges


def get_account_info(name):
    global user_info_global
    current_user_name = user_info_global.get('Name', None)
    if current_user_name is not None and name == current_user_name:
        return user_info_global

    user_info_global = user_info = win32net.NetUserGetInfo(None, name, 4)

    return user_info


def disable_account(name):
    user_info = get_account_info(name)

    # disable account
    user_info['flags'] = user_info.get('flags') | win32netcon.UF_ACCOUNTDISABLE

    try:
        win32net.NetUserSetInfo(None, name, 4, user_info)
    except pywintypes.error as e:
        print("ERROR: permission denied.")
        print(e)
        sys.exit(1)
    print("OK: account \"{}\" is disabled.".format(name))


def enable_account(name):
    user_info = get_account_info(name)

    # enable account
    user_info['flags'] = user_info.get('flags') & ~win32netcon.UF_ACCOUNTDISABLE

    try:
        win32net.NetUserSetInfo(None, name, 4, user_info)
    except pywintypes.error as e:
        print("ERROR: permission denied.")
        print(e)
        sys.exit(1)
    print("OK: account \"{}\" is enabled.".format(name))


if __name__ == '__main__':
    enable_account("guodong")
