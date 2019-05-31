#!/usr/bin/python
# encoding: utf-8
# -*- coding: utf8 -*-
"""
Created by PyCharm.
File Name:              LinuxBashShellScriptForOps:pyDataCompressionAndArchiving.py
Version:                0.0.1
Author:                 Guodong
Author Email:           dgdenterprise@gmail.com
URL:                    https://github.com/DingGuodong/LinuxBashShellScriptForOps
Download URL:           https://github.com/DingGuodong/LinuxBashShellScriptForOps/tarball/master
Create Date:            2018/2/13
Create Time:            10:53
Description:            Data Compression and Archiving with Python
Long Description:       tar compress file
                        It is useful for lots of log files to archive
References:             https://docs.python.org/2/library/archiving.html
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
import tarfile


def tar_compress_file(save, src):
    old_path = os.path.curdir

    if os.path.basename(src) == src:
        path = None
    else:
        path = os.path.dirname(src)
        src = os.path.basename(src)

    if path:
        os.chdir(path)

    # # All *open() methods are registered here.
    # OPEN_METH = {
    #     "tar": "taropen",  # uncompressed tar
    #     "gz": "gzopen",  # gzip compressed tar
    #     "bz2": "bz2open"  # bzip2 compressed tar
    # }
    with tarfile.open(save, "w:gz") as tar:
        tar.add(src)
        tar.close()

    os.chdir(old_path)


if __name__ == '__main__':
    tar_compress_file(r"C:\var\log\simple.tar.gz", r'C:\var\log\kissops_debug.log')
