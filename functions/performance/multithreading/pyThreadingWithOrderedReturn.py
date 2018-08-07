#!/usr/bin/python
# encoding: utf-8
# -*- coding: utf-8 -*-
"""
Created by PyCharm.
File Name:              LinuxBashShellScriptForOps:pyThreadingWithOrderedReturn.py
Version:                0.0.1
Author:                 Guodong
Author Email:           dgdenterprise@gmail.com
URL:                    https://github.com/DingGuodong/LinuxBashShellScriptForOps
Download URL:           https://github.com/DingGuodong/LinuxBashShellScriptForOps/tarball/master
Create Date:            2018/8/7
Create Time:            10:02
Description:            execute some tasks and return  result in order
Long Description:       有多个无参函数需要有序执行或者在返回时需要返回有序结果，有什么办法使得执行总时间最短？
比如函数x1,x2,x3,x4,x5五个函数，对应返回1、2、3、4、5五个结果，如何使得执行时间最短，但结果却是1、2、3、4、5？
期望：假设函数执行时间最长的为x4、时间为5s，那么在x4执行完，其他的x1，x2，x3，x5都应该执行完了，总时间应该为5s。

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
import random
from collections import defaultdict
from time import sleep


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
        print "Total time running {function_name}: {time_spent} seconds".format(function_name=func.func_name,
                                                                                time_spent=(time_end - time_begin))

        return result

    return function_timer


def fn_prompt(task_id):
    """
    用于在函数前后打印信息并支持传参的装饰器
    :param task_id:
    :return:
    """

    def prompt(func):
        from functools import wraps

        @wraps(func)
        def show_prompt(*args, **kwargs):
            print("task %s start" % task_id)
            result = func(*args, **kwargs)
            print("task %s finished" % task_id)

            return result

        return show_prompt

    return prompt


def fn_save_return(func):
    """
    使用装饰器非侵入函数而将函数结果保存
    :param func:
    :return:
    """
    from functools import wraps

    @wraps(func)
    def function_timer(*args, **kwargs):
        result = func(*args, **kwargs)
        results[func.func_name] = result
        return result

    return function_timer


@fn_save_return
@fn_timer
@fn_prompt(1)
def x1():
    sleep(random.randrange(2, 5))
    return 1


@fn_save_return
@fn_timer
@fn_prompt(2)
def x2():
    sleep(random.randrange(2, 5))
    return 2


@fn_save_return
@fn_timer
@fn_prompt(3)
def x3():
    sleep(random.randrange(2, 5))
    return 3


@fn_save_return
@fn_timer
@fn_prompt(4)
def x4():
    sleep(random.randrange(2, 5))
    return 4


@fn_save_return
@fn_timer
@fn_prompt(5)
def x5():
    sleep(random.randrange(2, 5))
    return 5


if __name__ == '__main__':
    import threading

    results = defaultdict()

    t1 = threading.Thread(target=x1)
    t2 = threading.Thread(target=x2)
    t3 = threading.Thread(target=x3)
    t4 = threading.Thread(target=x4)
    t5 = threading.Thread(target=x5)

    # for thread in (t1, t2, t3, t4, t5):
    #     thread.setDaemon(True)
    for thread in (t1, t2, t3, t4, t5):
        thread.start()
    for thread in (t1, t2, t3, t4, t5):
        if thread.isAlive():
            thread.join()

    print [data[1] for data in sorted(results.iteritems(), key=lambda x: x[0].split('x')[1])]
