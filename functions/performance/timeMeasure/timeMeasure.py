#!/usr/bin/python
# encoding: utf-8
# -*- coding: utf8 -*-
"""
Created by PyCharm.
File:               LinuxBashShellScriptForOps:timeMeasure.py
User:               Guodong
Create Date:        2017/1/16
Create Time:        9:50

Refer: http://www.jb51.net/article/63244.htm
Others:
    1. 'time' command in UNIX system or Linux system
    2. cProfile Module in Python
    3. line_profiler Module in Python
    4. memory_profiler Module in Python
 """


def fn_timer(function):
    from functools import wraps

    @wraps(function)
    def function_timer(*args, **kwargs):
        import time
        t0 = time.time()
        result = function(*args, **kwargs)
        t1 = time.time()
        print ("Total time running %s: %s seconds" %
               (function.func_name, str(t1 - t0))
               )
        return result

    return function_timer


@fn_timer
def _random_sort(n):
    import random
    return sorted([random.random() for i in range(n)])


if __name__ == "__main__":
    _random_sort(2000000)
