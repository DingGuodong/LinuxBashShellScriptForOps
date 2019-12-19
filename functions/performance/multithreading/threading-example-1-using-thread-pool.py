#!/usr/bin/python
# encoding: utf-8
# -*- coding: utf-8 -*-
"""
Created by PyCharm.
File Name:              LinuxBashShellScriptForOps:threading-example-using-thread-pool.py
Version:                0.0.1
Author:                 Guodong
Author Email:           dgdenterprise@gmail.com
URL:                    https://github.com/DingGuodong/LinuxBashShellScriptForOps
Download URL:           https://github.com/DingGuodong/LinuxBashShellScriptForOps/tarball/master
Create Date:            2019/1/29
Create Time:            16:48
Description:            run some func in a multi-thread way using ThreadPool
Long Description:       使用ThreadPool实现多线程运行函数
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
import sys
import time

from multiprocessing.pool import ThreadPool


def func(x):
    sys.stdout.write(str(x) + "\n")
    sys.stdout.flush()
    time.sleep(1)  # 假设func是一个耗时的函数，此处耗时1秒，则意味着使用多线程后耗时应该与1秒接近


if __name__ == '__main__':
    pool = ThreadPool(100)
    pool.map(func, range(1, 10))
    pool.close()  # 不再接受新的子进程加入到pool进程池，因此添加线程任务需要在pool.close()之前
    pool.join()  # 进入阻塞状态，等待子进程执行完毕后进入下一指令
