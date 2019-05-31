#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created by PyCharm.
File Name:              LinuxBashShellScriptForOps:sync-file-after-modified.py
Version:                0.0.1
Author:                 Guodong
Author Email:           dgdenterprise@gmail.com
URL:                    https://github.com/DingGuodong/LinuxBashShellScriptForOps
Download URL:           https://github.com/DingGuodong/LinuxBashShellScriptForOps/tarball/master
Create Date:            2019/3/7
Create Time:            17:26
Description:            sync files to share folder after modified on MS Windows
Long Description:       
References:             
Prerequisites:          []
Development Status:     3 - Alpha, 5 - Production/Stable
Environment:            Console
Intended Audience:      System Administrators, Developers, End Users/Desktop
License:                Freeware, Freely Distributable
Natural Language:       English, Chinese (Simplified)
Operating System:       POSIX :: Linux, Microsoft :: Windows
Programming Language:   Python :: 3

Topic:                  Utilities
 """
import os


def to_unicode_or_bust(obj, encoding='utf-8'):
    # the function convert non-unicode object to unicode object
    if isinstance(obj, str):
        if not isinstance(obj, str):
            obj = str(obj, encoding)

    return obj


def to_str_or_bust(obj, encoding='utf-8'):
    # the function convert unicode object to str object
    if isinstance(obj, str):
        if isinstance(obj, str):
            obj = obj.encode(encoding)

    return obj


remote_share_folder = r"\\192.168.88.29\资产管理文档"
local_folder = r"D:\C盘桌面未整理\EBT\admin-playbook\ebt-company-project" \
               r"\20181203-sunglink-资产统计\与财务部共享目录资产台账"

remote_share_folder = to_unicode_or_bust(remote_share_folder)
local_folder = to_unicode_or_bust(local_folder)

if os.path.isdir(local_folder):
    for top, dirs, nondirs in os.walk(local_folder, followlinks=True):
        for item in nondirs:
            local_file = os.path.join(top, item)
            if item.startswith("~$"):  # Owner File
                continue
            remote_file = os.path.join(remote_share_folder, item)

            lf_mtime = os.path.getmtime(local_file)
            rf_mtime = os.path.getmtime(remote_file)

            if lf_mtime > rf_mtime:
                print("local file newer: %s" % local_file)
            elif lf_mtime == rf_mtime:
                print("identical")
            else:
                print("remote file newer: %s" % rf_mtime)
        break
