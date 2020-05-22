#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created by PyCharm.
File Name:              LinuxBashShellScriptForOps:test-system-limit-nofile-nproc.py
Version:                0.0.1
Author:                 dgden
Author Email:           dgdenterprise@gmail.com
URL:                    https://github.com/DingGuodong/LinuxBashShellScriptForOps
Download URL:           https://github.com/DingGuodong/LinuxBashShellScriptForOps/tarball/master
Create Date:            2020/5/22
Create Time:            8:57
Description:            test system resource limits, such as nofile, nproc
Long Description:       ulimit
References:             [IOError: [Errno 24] Too many open files](https://stackoverflow.com/questions/18280612/ioerror-errno-24-too-many-open-files)
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
from __future__ import print_function

import os
import resource
import sys
from multiprocessing import Process

import time


def create_file(filename):
    try:
        res = open(filename, 'wb', buffering=0)
    except IOError as e:
        print(e, file=sys.stderr)
        sys.exit(1)
    return res


def test_nofile(count=-1):
    nofile_soft, nofile_hard = resource.getrlimit(resource.RLIMIT_NOFILE)

    # allow user test nofile count
    if count == -1:
        nofile_count_test = nofile_soft
        # tune nofile value from soft to hard
        resource.setrlimit(resource.RLIMIT_NOFILE, (nofile_hard, nofile_hard))
    else:
        nofile_count_test = count

    fp_obj_list = list()
    for x in range(nofile_count_test):
        cur_filename = "ptf_" + str(x)
        print("creating file: {}".format(cur_filename))
        fp_obj = create_file(cur_filename)
        fp_obj_list.append(fp_obj)  # save opened fps into list to hold on


def minimal_process():
    while 1:
        print("current sub process id (pid) is: {}".format(os.getpid()))
        time.sleep(1)


def create_process():
    res = Process(target=minimal_process)
    return res


def test_nproc(count=-1):
    nproc_soft, nproc_hard = resource.getrlimit(resource.RLIMIT_NPROC)

    # allow user test nofile count
    if count == -1:
        nproc_count_test = nproc_soft
        # tune nproc value from soft to hard
        resource.setrlimit(resource.RLIMIT_NPROC, (nproc_hard, nproc_hard))
    else:
        nproc_count_test = count

    proc_obj_list = list()
    for x in range(nproc_count_test):
        proc_obj = create_process()
        proc_obj_list.append(proc_obj)  # save proc obj into list to ready for run, this step won't create real process

    for x in proc_obj_list:
        x.start()  # start the process, create real process in system


if __name__ == '__main__':
    print("current process id (pid) is: {}".format(os.getpid()))

    test_nofile(2048)
    test_nproc(50)

    # give user to check using `lsof` or 'ps' etc.
    time.sleep(1000)
