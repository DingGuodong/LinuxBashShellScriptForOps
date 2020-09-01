#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created by PyCharm.
File Name:              LinuxBashShellScriptForOps:threading-example-3-using-thread-pool.py
Version:                0.0.1
Author:                 dgden
Author Email:           dgdenterprise@gmail.com
URL:                    https://github.com/DingGuodong/LinuxBashShellScriptForOps
Download URL:           https://github.com/DingGuodong/LinuxBashShellScriptForOps/tarball/master
Create Date:            2020/9/1
Create Time:            13:40
Description:            
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
import time
from concurrent.futures import ThreadPoolExecutor, as_completed


def fake_get_html(times):
    time.sleep(times)
    print("get page {} success".format(times))
    return times


executor = ThreadPoolExecutor(max_workers=2)
task1 = executor.submit(fake_get_html, 2)

while True:
    if task1.done():
        print(task1.result())
        break
    else:
        time.sleep(1)

task2 = [executor.submit(fake_get_html, url) for url in [3, 2, 1]]
for subtask in as_completed(task2):
    data = subtask.result()
    print(data)
