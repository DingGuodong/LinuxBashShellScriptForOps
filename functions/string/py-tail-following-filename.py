#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created by PyCharm.
File Name:              LinuxBashShellScriptForOps:py-tail-following-filename.py
Version:                0.0.1
Author:                 dgden
Author Email:           dgdenterprise@gmail.com
URL:                    https://github.com/DingGuodong/LinuxBashShellScriptForOps
Download URL:           https://github.com/DingGuodong/LinuxBashShellScriptForOps/tarball/master
Create Date:            2019/8/29
Create Time:            10:46
Description:            a python script like tail -f of GNU coreutils
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
import time


def tail_forever_deprecated(filename, limit=10):
    """
    tail can NOT remember the last position it has read, so it will always show the line it had read in some case
    and not act well on Microsoft Windows
    :param filename:
    :param limit:
    :return:
    """
    import subprocess
    res = subprocess.Popen(["tail", "-f", filename, "-n", str(limit)], stdout=subprocess.PIPE)
    while 1:
        line = res.stdout.readline()
        print(line),


def get_content_from_file(filename, offset=0):
    with open(filename, 'r') as fp:
        fp.seek(offset)
        for line in fp:
            print(line),


def write_meta(filename):
    file_size = os.stat(filename).st_size
    file_ino = os.stat(filename).st_ino
    file_meta = filename.replace(os.path.basename(filename), "." + os.path.basename(filename) + ".offset")
    with open(file_meta, 'w') as fp:
        fp.write(" ".join([filename, str(file_ino), str(file_size)]))


def read_meta(filename):
    file_meta = filename.replace(os.path.basename(filename), "." + os.path.basename(filename) + ".offset")
    with open(file_meta, 'r') as fp:
        return int(fp.read().split()[-1])


def tail_forever(filename):
    file_meta = filename.replace(os.path.basename(filename), "." + os.path.basename(filename) + ".offset")
    file_size = 0

    if not os.path.exists(file_meta):
        write_meta(filename)
    else:
        file_size = read_meta(filename)

    while 1:
        current_file_size = os.stat(filename).st_size
        if file_size < current_file_size:
            get_content_from_file(filename, file_size)
            file_size = current_file_size
        time.sleep(0.25)


if __name__ == '__main__':
    tail_forever(__file__)

