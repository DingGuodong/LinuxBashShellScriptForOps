#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created by PyCharm.
File Name:              LinuxBashShellScriptForOps:clean-old-backups-with-given-directory.py
Version:                0.0.1
Author:                 Guodong
Author Email:           dgdenterprise@gmail.com
URL:                    https://github.com/DingGuodong/LinuxBashShellScriptForOps
Download URL:           https://github.com/DingGuodong/LinuxBashShellScriptForOps/tarball/master
Create Date:            2019/3/12
Create Time:            15:12
Description:            clean old backups with given directory
Long Description:
References:             
Prerequisites:          pip install -U python-dateutil
Development Status:     3 - Alpha, 5 - Production/Stable
Environment:            Console
Intended Audience:      System Administrators, Developers, End Users/Desktop
License:                Freeware, Freely Distributable
Natural Language:       English, Chinese (Simplified)
Operating System:       POSIX :: Linux, Microsoft :: Windows
Programming Language:   Python :: 3

Topic:                  Utilities
 """

import datetime
import os
import time

from dateutil.relativedelta import relativedelta


def to_unicode_or_bust(obj, encoding='utf-8'):
    """
    convert non-unicode object to unicode object
    :param obj: str object or unicode
    :param encoding:
    :return:
    """
    if isinstance(obj, str):
        if not isinstance(obj, str):
            obj = str(obj, encoding)

    return obj


def to_str_or_bust(obj, encoding='utf-8'):
    """
    convert unicode object to str object
    :param obj: unicode object or str
    :param encoding:
    :return:
    """
    if isinstance(obj, str):
        if isinstance(obj, str):
            obj = obj.encode(encoding)

    return obj


def clean_old_backups(path, ext="bak", days=30):
    """
    clean old backups with given directory, return counts of files deleted
    :param path: backup directory
    :param ext: extension of backup file
    :param days: days of backup saves
    :return:
    """
    path = to_unicode_or_bust(path)
    if not os.path.exists(path):
        raise RuntimeError("Error: cannot access \'%s\': No such file or directory" % path)

    timestamp_before_save_days = time.mktime((datetime.datetime.today() + relativedelta(days=-days)).timetuple())

    count_removed = 0
    for top, dirs, nondirs in os.walk(path):
        for filename in nondirs:
            if filename.endswith(ext):
                filepath = os.path.join(top, filename)
                if os.path.getmtime(filepath) < timestamp_before_save_days:
                    count_removed += 1
                    os.remove(filepath)

    return count_removed


if __name__ == '__main__':
    backup_source = r'D:\Microsoft SQL Server Backup'
    backup_extension = "bak"
    save_days = 30

    print(clean_old_backups(backup_source, backup_extension, save_days))
