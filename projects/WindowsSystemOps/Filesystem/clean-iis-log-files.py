#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created by PyCharm.
File Name:              LinuxBashShellScriptForOps:clean-iis-log-files.py
Version:                0.0.1
Author:                 dgden
Author Email:           dgdenterprise@gmail.com
URL:                    https://github.com/DingGuodong/LinuxBashShellScriptForOps
Download URL:           https://github.com/DingGuodong/LinuxBashShellScriptForOps/tarball/master
Create Date:            2020/2/2
Create Time:            9:12
Description:            clean Microsoft IIS default logs
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


def get_size_of_path(path):
    if os.path.isdir(path):
        size = 0
        for top, dirs, nondirs in os.walk(path):
            for filename in nondirs:
                full_path = os.path.join(top, filename)
                size += os.path.getsize(full_path)
        return size


def do_clean_logs(path, ends=".log"):
    if os.path.isdir(path):
        for top, dirs, nondirs in os.walk(path):
            for filename in nondirs:
                if filename.endswith(ends):
                    curr_file = os.path.join(top, filename)
                    try:
                        os.remove(curr_file)
                    except WindowsError:
                        print("file %s is opened(in use), skipped" % curr_file)
            for directory in dirs:
                curr_dir = os.path.join(top, directory)
                if len(os.listdir(curr_dir)) == 0:
                    os.removedirs(curr_dir)


if __name__ == '__main__':
    MAX_LOG_SIZE = 400000000
    iis_logs_path = r"C:\inetpub\logs\LogFiles"
    log_size = get_size_of_path(iis_logs_path)
    if log_size > MAX_LOG_SIZE:
        do_clean_logs(iis_logs_path)
    else:
        print("directory %s skipped" % iis_logs_path)
