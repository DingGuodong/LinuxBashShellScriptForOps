#!/usr/bin/python
# encoding: utf-8
# -*- coding: utf8 -*-
"""
Created by PyCharm.
File:               LinuxBashShellScriptForOps:pyWMIGetSystemInformation.py
User:               Guodong
Create Date:        2017/8/18
Create Time:        9:24
Description:        Not recommend to use it, can NOT trace, see more by 'help('wmi')'
References:         https://pypi.python.org/pypi/WMI/1.4.9
                    http://timgolden.me.uk/python/wmi/tutorial.html
                    http://timgolden.me.uk/python/wmi/cookbook.html
 """
import wmi


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
    except Exception:
        encoding = 'ascii'
    return encoding


DEFAULT_LOCALE_ENCODING = get_system_encoding()

c = wmi.WMI()
print c.Win32_ComputerSystem()[0].Name
DRIVE_TYPES = {
    0: "Unknown",
    1: "No Root Directory",
    2: "Removable Disk",
    3: "Local Disk",
    4: "Network Drive",
    5: "Compact Disc",
    6: "RAM Disk"
}
for disk in c.Win32_LogicalDisk():
    print disk.Caption, DRIVE_TYPES[disk.DriveType], disk.Description, disk.ProviderName or ""
for disk in c.Win32_LogicalDisk(DriveType=3):
    print disk.Caption, "%0.2f%% free" % (100.0 * long(disk.FreeSpace) / long(disk.Size))
