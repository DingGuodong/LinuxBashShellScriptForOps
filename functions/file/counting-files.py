#!/usr/bin/python
# encoding: utf-8
# -*- coding: utf-8 -*-
"""
Created by PyCharm.
File Name:              LinuxBashShellScriptForOps:counting-files.py
Version:                0.0.1
Author:                 Guodong
Author Email:           dgdenterprise@gmail.com
URL:                    https://github.com/DingGuodong/LinuxBashShellScriptForOps
Download URL:           https://github.com/DingGuodong/LinuxBashShellScriptForOps/tarball/master
Create Date:            2019/2/18
Create Time:            12:17
Description:            count files with a file extension
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


def get_files_with_ending(path=".", ending="not_exist_at_all"):
    count = 0
    # files = os.path.join(path, "files_list.txt")
    files = "_files_list.txt"
    with open(files, 'w') as fp:
        for top, dirs, nondirs in os.walk(path, followlinks=True):
            for item in nondirs:
                if item.endswith(ending):
                    fpath = os.path.abspath(os.path.join(top, item))
                    fp.write(fpath + '\n')
                    count += 1
    return count, files


if __name__ == '__main__':
    print(get_files_with_ending('.', 'py'))
