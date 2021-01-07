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

"永远不要使用 except: 语句来捕获所有异常, 也不要捕获 Exception 或者 StandardError ,
除非你打算重新触发该异常, 或者你已经在当前线程的最外层(记得还是要打印一条错误消息).
在异常这方面, Python非常宽容, except: 真的会捕获包括Python语法错误在内的任何错误.
使用 except: 很容易隐藏真正的bug." -- [《Google Python 风格指南》]
 (https://google-styleguide.readthedocs.io/zh_CN/latest/google-python-styleguide/python_language_rules.html)

Tips: exception不要太宽泛，且try-except应该放在发生exception最近的地方，不然debug起来可能比较费劲。

"""


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


def fn_timer_py2py3(func):
    """
    测量函数执行所用时间的装饰器
    https://stackoverflow.com/questions/8885663/how-to-format-a-floating-number-to-fixed-width-in-python
    :param func:
    :return:
    """
    from functools import wraps

    @wraps(func)
    def func_timer(*args, **kwargs):
        import time
        time_begin = time.time()
        result = None
        try:
            result = func(*args, **kwargs)
        except Exception as e:
            print(e.message)
        time_end = time.time()
        print("Total time running {func_name}: {time_spent:16.8f} seconds".format(func_name=func.__name__,
                                                                                  time_spent=time_end - time_begin))
        return result

    return func_timer


@fn_timer_py2py3
@fn_timer
def _random_sort(n):
    import random
    return sorted([random.random() for _ in range(n)])


if __name__ == "__main__":
    _random_sort(2000000)
