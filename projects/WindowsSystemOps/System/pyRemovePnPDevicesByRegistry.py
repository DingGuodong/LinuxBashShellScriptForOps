#!/usr/bin/python
# encoding: utf-8
# -*- coding: utf-8 -*-
"""
Created by PyCharm.
File Name:              LinuxBashShellScriptForOps:pyRemovePnPDevicesByRegistry.py
Version:                0.0.1
Author:                 Guodong
Author Email:           dgdenterprise@gmail.com
URL:                    https://github.com/DingGuodong/LinuxBashShellScriptForOps
Download URL:           https://github.com/DingGuodong/LinuxBashShellScriptForOps/tarball/master
Create Date:            2019/1/14
Create Time:            15:46
Description:            remove all uPnP devices by operating Windows Registry
Long Description:       删除 “控制面板\所有控制面板项\设备和打印机”中的多媒体设备
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

import _winreg


def get_system_encoding():
    import codecs
    import locale
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


def get_sub_keys():
    keys = list()
    reg_key = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE, sub_key_name)

    try:
        for index in xrange(65535):
            sub_key = _winreg.EnumKey(reg_key, index)
            keys.append(sub_key)
    except WindowsError:
        # System Error Codes (0-499)
        # https://docs.microsoft.com/en-us/windows/desktop/debug/system-error-codes--0-499-
        # No more data is available.
        pass

    return keys


if __name__ == '__main__':
    # 计算机\HKEY_LOCAL_MACHINE\SYSTEM\ControlSet001\Enum\SWD\DAFUPnPProvider
    sub_key_name = r"SYSTEM\ControlSet001\Enum\SWD\DAFUPnPProvider"

    try:
        reg_key = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE, sub_key_name)
        for key in get_sub_keys():
            _winreg.DeleteKey(reg_key, key)
    except Exception as e:
        print e,
        if e.args[0] == 5:
            print "[Error 5], ERROR_ACCESS_DENIED, Access is denied."
            print "Run as Administrator ?"

    # disable Windows service "SSDPSRV", "upnphost"
