#!/usr/bin/python
# encoding: utf-8
# -*- coding: utf8 -*-
"""
Created by PyCharm.
File Name:              LinuxBashShellScriptForOps:pyRenameFileByBatch.py
Version:                0.0.1
Author:                 Guodong
Author Email:           dgdenterprise@gmail.com
URL:                    https://github.com/DingGuodong/LinuxBashShellScriptForOps
Download URL:           https://github.com/DingGuodong/LinuxBashShellScriptForOps/tarball/master
Create Date:            2018/3/5
Create Time:            16:21
Description:            python rename file's extension by batch
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
import os
import re
from collections import Iterable


def rename_files_batch(path, new_extension, exclude_pattern="init"):
    os.chdir(path)
    pattern = re.compile(exclude_pattern)
    # TODO(Guodong Ding) use gevent or multi-threading will get better performance
    for top, dirs, nondirs in os.walk(path):
        for filename in nondirs:
            if not pattern.search(filename):
                (old_filename, old_extension) = os.path.splitext(filename)
                os.renames(filename, old_filename + new_extension)


if __name__ == '__main__':
    path_to_deal = [
        r'C:\Users\Guodong\PycharmProjects\LinuxBashShellScriptForOps\projects\LinuxSystemOps\Services\SysV\CentOS',
        r'C:\Users\Guodong\PycharmProjects\LinuxBashShellScriptForOps\projects\LinuxSystemOps\Services\SysV\Ubuntu'
    ]

    if isinstance(path_to_deal, Iterable):
        for dir_path in path_to_deal:
            rename_files_batch(dir_path, ".sysv", "init|func")
    else:
        rename_files_batch(path_to_deal, ".sysv", "init|func")
