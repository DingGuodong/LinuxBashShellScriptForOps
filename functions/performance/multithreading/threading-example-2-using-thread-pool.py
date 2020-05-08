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
from concurrent.futures import ThreadPoolExecutor  # Python version 2.6, 2.7 do not have module concurrent.futures


def fn_timer(func):
    """
    测量函数执行所用时间的装饰器
    :param func:
    :return:
    """
    from functools import wraps

    @wraps(func)
    def function_timer(*args, **kwargs):
        import time
        time_begin = time.time()
        result = func(*args, **kwargs)
        time_end = time.time()
        print("Total time running {func_name}: {time_spent} seconds".format(func_name=func.__name__,
                                                                            time_spent=(time_end - time_begin)))

        return result

    return function_timer


def fib(n):
    """
    Successione di Fibonacci 菲波拿契数列

    在数学上，费波那契数列是以递归的方法来定义：
    F{0}=0
    F{1}=1
    F{n}=F{n-1}+F{n-2}}（n≧2）

    https://zh.wikipedia.org/zh-hant/斐波那契数列

    :param n:
    :return:
    """
    if n <= 2:
        return 1
    return fib(n - 1) + fib(n - 2)  # use recursion will lead to low performance(lowest)


def fib1(n):
    a, b = 1, 1
    for i in range(3, n + 1):  # this implement has highest performance
        a, b = b, a + b
    return b


def fib2_set(n):
    a, b, c = 0, 1, 0
    while True:  # this implement has medium performance
        if c > n:
            return
        yield a

        a, b = b, a + b
        c += 1


def fib2_get(y):
    flag = True
    result = None
    while flag:
        try:
            result = next(y)
        except StopIteration:
            flag = False
    return result


def fib3(n):
    fibs = [0, 1]
    for i in range(n - 2):
        fibs.append(fibs[-2] + fibs[-1])
    return sum(fibs)


@fn_timer
def test_thread_pool():
    """
    works fine in Python3, not works in Python2
    :return:
    """
    with ThreadPoolExecutor(max_workers=2 * 5) as ex:  # max_workers = (cpu_count() or 1) * 5
        workers = []
        for x in range(5):
            workers.append(ex.submit(fib, 30 + x))

        res = [worker.result() for worker in workers]

    print(res)


@fn_timer
def test_no_thread_pool():
    print([fib(x) for x in range(30, 30 + 5)])


@fn_timer
def test_no_thread_pool_1():
    print([fib1(x) for x in range(30, 30 + 5)])


if __name__ == '__main__':
    test_no_thread_pool()
    test_no_thread_pool_1()
    test_thread_pool()
