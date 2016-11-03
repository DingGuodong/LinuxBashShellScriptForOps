#!/usr/bin/python
# encoding: utf-8
# -*- coding: utf8 -*-
"""
Created by PyCharm.
File:               LinuxBashShellScriptForOps:threadingExample.py
User:               Guodong
Create Date:        2016/11/1
Create Time:        18:14
 """
import threading
import time
from functools import wraps


def fn_timer(function):
    @wraps(function)
    def function_timer(*args, **kwargs):
        t0 = time.time()
        result = function(*args, **kwargs)
        t1 = time.time()
        print ("Total time running %s: %s seconds" %
               (function.func_name, str(t1 - t0))
               )
        return result

    return function_timer


@fn_timer
def jobsA(para):
    print "Do jobs A"
    jobsACount = 5
    for job in range(jobsACount):
        print "Do sub job in jobs A %d" % job
        if para is True:
            print "para(%s) is True" % para
        else:
            print "para(%s) is False" % para
        time.sleep(2)


@fn_timer
def jobsB(para):
    print "Do jobs B"
    jobsBCount = 10
    for job in range(jobsBCount):
        print "Do sub job in jobs B %d" % job
        if para is True:
            print "para(%s) is True" % para
        else:
            print "para(%s) is False" % para
        time.sleep(1)


threadingPool = list()
threading_1 = threading.Thread(target=jobsA, args=(True,))
threading_2 = threading.Thread(target=jobsB, args=(False,))
threadingPool.append(threading_1)
threadingPool.append(threading_2)

if __name__ == '__main__':
    print "All jobs is start! at %s" % time.ctime()
    for thread in threadingPool:
        thread.setDaemon(True)
        thread.start()

    thread.join()

    print "All jobs is done! at %s" % time.ctime()
