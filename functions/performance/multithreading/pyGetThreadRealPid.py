#!/usr/bin/python
# encoding: utf-8
# -*- coding: utf8 -*-
"""
Created by PyCharm.
File Name:              LinuxBashShellScriptForOps:pyGetThreadRealPid.py
Version:                0.0.1
Author:                 Guodong
Author Email:           dgdenterprise@gmail.com
URL:                    https://github.com/DingGuodong/LinuxBashShellScriptForOps
Download URL:           https://github.com/DingGuodong/LinuxBashShellScriptForOps/tarball/master
Create Date:            2017/11/24
Create Time:            11:54
Description:            get real pid of thread in kernel layer
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
import threading
import time

import psutil


def long_time_task(sleep_seconds=30):
    print threading.current_thread().name,
    print threading.current_thread().ident  # works on Windows, real pid in Windows kernel layer
    keep_running_flag = True
    count = 0
    while keep_running_flag:
        count += 1
        if sleep_seconds >= 1:
            if count > sleep_seconds:
                break
            time.sleep(1)
        else:
            time.sleep(abs(sleep_seconds))
            keep_running_flag = False
    return True


threadingPool = list()
threading_1 = threading.Thread(target=long_time_task, args=(20,))
threading_2 = threading.Thread(target=long_time_task, args=(20,))
threadingPool.append(threading_1)
threadingPool.append(threading_2)

if __name__ == '__main__':
    print os.getpid()

    for thread in threadingPool:
        thread.setDaemon(True)
        thread.start()

    for process in psutil.process_iter():
        if process.pid == os.getpid():
            if process.num_threads() != 0:
                for pthread in process.threads():
                    print pthread

    thread.join()
