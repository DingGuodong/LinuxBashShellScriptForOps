#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created by PyCharm.
File Name:              LinuxBashShellScriptForOps:readers-writers-problem.py
Version:                0.0.1
Author:                 dgden
Author Email:           dgdenterprise@gmail.com
URL:                    https://github.com/DingGuodong/LinuxBashShellScriptForOps
Download URL:           https://github.com/DingGuodong/LinuxBashShellScriptForOps/tarball/master
Create Date:            2020/7/6
Create Time:            11:26
Description:            Python 3 implementation of the Readers-writers problem
Long Description:       [does not get the point]
References:             [Reader Writer Lock](https://pypi.org/project/readerwriterlock/)
                        [Readers–writers problem](https://en.wikipedia.org/wiki/Readers%e2%80%93writers_problem)
                        [使用读写锁加速Python多线程应用](https://zhuanlan.zhihu.com/p/82398406)
Prerequisites:          pip install readerwriterlock
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
import threading

WEEKDAYS = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
today = 0


def regular_lock_example():
    marker = threading.Lock()

    def calendar_reader(id_number):
        global today
        name = 'Reader-' + str(id_number)
        while today < len(WEEKDAYS) - 1:
            marker.acquire()
            print(name, 'sees that today is', WEEKDAYS[today])
            marker.release()

    def calender_writer(id_number):
        global today
        name = 'Write-' + str(id_number)
        while today < len(WEEKDAYS) - 1:
            marker.acquire()
            today = (today + 1) % 7
            print(name, 'updated date to ', WEEKDAYS[today])

    #  create ten reader threads
    for i in range(10):
        threading.Thread(target=calendar_reader, args=(i,)).start()
    #  ...but only two writer threads
    for i in range(2):
        threading.Thread(target=calender_writer, args=(i,)).start()


def rwlock_example():
    from readerwriterlock import rwlock

    marker = rwlock.RWLockFair()

    def calendar_reader(id_number):
        global today
        read_marker = marker.gen_rlock()
        name = 'Reader-' + str(id_number)
        while today < len(WEEKDAYS) - 1:
            read_marker.acquire()
            sys.stdout.write(" ".join((str(name), 'sees that today is', WEEKDAYS[today], '-read count:',
                                       str(read_marker.c_rw_lock.v_read_count), '\n')))
            sys.stdout.flush()
            read_marker.release()

    def calender_writer(id_number):
        global today
        write_marker = marker.gen_wlock()
        name = 'Write-' + str(id_number)
        while today < len(WEEKDAYS) - 1:
            write_marker.acquire()
            today = (today + 1) % 7
            sys.stdout.write(" ".join((str(name), 'updated date to ', WEEKDAYS[today], '\n')))
            sys.stdout.flush()
            write_marker.release()

    #  create ten reader threads
    for i in range(10):
        threading.Thread(target=calendar_reader, args=(i,)).start()
    #  ...but only two writer threads
    for i in range(2):
        threading.Thread(target=calender_writer, args=(i,)).start()


if __name__ == '__main__':
    rwlock_example()
