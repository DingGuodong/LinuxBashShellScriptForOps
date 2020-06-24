#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created by PyCharm.
File Name:              LinuxBashShellScriptForOps:python-handle-stdin-and-files.py
Version:                0.0.1
Author:                 dgden
Author Email:           dgdenterprise@gmail.com
URL:                    https://github.com/DingGuodong/LinuxBashShellScriptForOps
Download URL:           https://github.com/DingGuodong/LinuxBashShellScriptForOps/tarball/master
Create Date:            2020/6/24
Create Time:            10:23
Description:            fileinput quick references
Long Description:       handle stdin, multiple files, replace inplace
References:             [fileinput — Iterate over lines from multiple input streams](https://docs.python.org/3/library/fileinput.html)
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

import _locale
import fileinput

# override default locale
_locale._getdefaultlocale = (lambda *args: ['en_US', 'utf8'])


def handle_multi_files():
    with fileinput.input(files=(__file__, __file__)) as f:
        for line in f:
            print(line)


def handle_stdin():
    with fileinput.input() as f:
        for line in f:
            print(line)


def backup_and_process():
    """
    KNOWN ISSUE: files' encoding must be same with system's encoding(locale.getpreferredencoding())
        M1: set interpreter options '-X utf8'
        M2: override locale: import _locale;_locale._getdefaultlocale = (lambda *args: ['en_US', 'utf8'])
    backup files and replace string inplace
    :return:
    :rtype:
    """
    f = fileinput.input(files=__file__, backup=".bak", inplace=True)
    for line in f:
        print(line.replace('src string', 'dst string')),  # print() is essential


if __name__ == '__main__':
    backup_and_process()
