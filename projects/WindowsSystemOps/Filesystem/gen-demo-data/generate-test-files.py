#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created by PyCharm.
File Name:              LinuxBashShellScriptForOps:generate-test-files.py
Version:                0.0.1
Author:                 dgden
Author Email:           dgdenterprise@gmail.com
URL:                    https://github.com/DingGuodong/LinuxBashShellScriptForOps
Download URL:           https://github.com/DingGuodong/LinuxBashShellScriptForOps/tarball/master
Create Date:            2020/11/2
Create Time:            16:32
Description:            generate test files named such as 'XXXX_XXXX_backup_2020_10_30_000001_7326777.bak.rar'
Long Description:       generate test files for clean old backups v2.1
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

import time


def create_blank_file(name):
    with open(name, 'w') as fp:
        fp.write('')


def clean_files(ext=".bak", prefix="", ):
    basepath = os.path.abspath(os.path.dirname(__file__))
    for item in os.listdir(basepath):
        if item.startswith(prefix) and item.endswith(ext):
            os.remove(item)


def generate_daily_files_with_time_named(basename, ext, format_, begin, end, ):
    if basename == "":
        basename = "test"

    if format_ == "":
        format_ = "%Y_%d_%m"
    else:
        if " " in format_:
            format_.replace(" ", "_")

    if begin == "":
        begin = time.time() - 35 * 24 * 3600
    else:
        begin = time.mktime(time.strptime(begin, format_))

    if end == "" or end == 'now':
        end = time.time()
    else:
        end = time.mktime(time.strptime(end, format_))

    now = begin
    while True:
        name = "_".join((basename, time.strftime(format_, time.localtime(now)))) + ext
        if now <= end:
            create_blank_file(name)
            now = now + 86400
        else:
            break


if __name__ == '__main__':
    # clean_files(".txt", "_backup")
    clean_files(".txt")
    clean_files(".log")
    generate_daily_files_with_time_named("p_backup", ".txt", "%Y_%m_%d_%H%M%S", "2020_08_29_092530", "now")
