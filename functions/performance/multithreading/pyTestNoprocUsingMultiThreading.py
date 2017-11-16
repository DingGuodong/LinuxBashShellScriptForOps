#!/usr/bin/python
# encoding: utf-8
# -*- coding: utf8 -*-
"""
Created by PyCharm.
File Name:              LinuxBashShellScriptForOps:pyTestNoprocUsingMultiThreading.py
Version:                0.0.1
Author:                 Guodong
Author Email:           dgdenterprise@gmail.com
URL:                    https://github.com/DingGuodong/LinuxBashShellScriptForOps
Download URL:           https://github.com/DingGuodong/LinuxBashShellScriptForOps/tarball/master
Create Date:            2017/11/16
Create Time:            14:16
Description:            test how many processes(include threads) can a user(not root) create
Long Description:       nproc(max user processes) is include all process and thread number of same user,
                        root is no limit usually

                        The threads will have the same PID but only when viewed from above.
                        What you (as a user) call a PID is not what the kernel (looking from below) calls a PID.
                        In the kernel, each thread has it's own ID, called a PID (although it would possibly make more
                        sense to call this a TID, or thread ID) and they also have a TGID (thread group ID) which
                        is the PID of the thread that started the whole process.
                        Simplistically, when a new process is created, it appears as a thread where
                        both the PID and TGID are the same (new) number.
                        When a thread starts another thread, that started thread gets its own PID (so the scheduler can
                        schedule it independently) but it inherits the TGID from the original thread.
                        That way, the kernel can happily schedule threads independent of what process they belong to,
                        while processes (thread group IDs) are reported to you.

References:             https://stackoverflow.com/questions/9305992/if-threads-share-the-same-pid-how-can-they-be-identified
                        https://unix.stackexchange.com/questions/102951/why-do-top-and-ps-show-different-pids-for-the-same-processes
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
import logging.handlers
import os
import sys
import threading
import time

log_name = "sample"
log_filename = "sample.log"
log_file_max_size = 104857600  # 100MB
log_file_save_number = 10  # save 10 log file
log_file_path = os.path.abspath(os.path.join(os.path.curdir, log_filename))
log_file_encoding = 'utf-8'
log_formatter = logging.Formatter(fmt="%(asctime)s %(filename)s:%(lineno)d %(name)s %(levelname)s: %(message)s",
                                  datefmt=None)  # datefmt=None means "%Y-%m-%d %H:%M:%S" with %03d msecs, \
# such as 2017-11-16 14:40:17,555

file_handler = logging.handlers.RotatingFileHandler(log_file_path, maxBytes=log_file_max_size,
                                                    backupCount=log_file_save_number,
                                                    encoding=log_file_encoding)
file_handler.setFormatter(log_formatter)
stream_handler = logging.StreamHandler(sys.stderr)

logger = logging.getLogger(log_name)
logger.addHandler(file_handler)
logger.addHandler(stream_handler)
logger.setLevel(logging.DEBUG)


def fn_timer(func):
    from functools import wraps

    @wraps(func)
    def function_timer(*args, **kwargs):
        import time
        time_begin = time.time()
        result = func(*args, **kwargs)
        time_end = time.time()
        print "Total time running {function_name}: {time_spent} seconds".format(function_name=func.func_name,
                                                                                time_spent=(time_end - time_begin))

        return result

    return function_timer


def long_time_task(sleep_seconds=30):
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
start_threading = int(1024 - 121)  # 121 is "ps -u $USER -fL | wc -l"
for _ in range(start_threading):
    threadingPool.append(threading.Thread(target=long_time_task, args=(30,)))

if __name__ == '__main__':
    print "All jobs is start! at %s" % time.ctime()
    time_start = time.time()
    for thread in threadingPool:
        thread.setDaemon(True)
        thread.start()

    thread.join()
    time_finished = time.time()
    print "All jobs is done! at %s" % time.ctime()
    print "All jobs take %03f" % (time_finished - time_start)
