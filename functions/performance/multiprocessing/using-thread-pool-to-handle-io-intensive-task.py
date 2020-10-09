#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created by PyCharm.
File Name:              LinuxBashShellScriptForOps:using-thread-pool-to-handle-io-intensive-task.py
Version:                0.0.1
Author:                 dgden
Author Email:           dgdenterprise@gmail.com
URL:                    https://github.com/DingGuodong/LinuxBashShellScriptForOps
Download URL:           https://github.com/DingGuodong/LinuxBashShellScriptForOps/tarball/master
Create Date:            2020/10/9
Create Time:            11:57
Description:            using thread pool to handle io intensive task
Long Description:       take ping many domains for example
References:             
Prerequisites:          []
Development Status:     3 - Alpha, 5 - Production/Stable
Environment:            Console
Intended Audience:      System Administrators, Developers, End Users/Desktop
License:                Freeware, Freely Distributable
Natural Language:       English, Chinese (Simplified)
Operating System:       POSIX :: Linux, Microsoft :: Windows
Programming Language:   Python :: 3
Topic:                  Utilities
 """
from multiprocessing.pool import ThreadPool

import ping3  # only can be used in python 3 interpreter

try:
    from queue import Queue  # Microsoft Windows test passed
except ImportError:
    try:
        from Queue import Queue  # Linux test passed
    except ImportError:
        from multiprocessing import Queue  # others

# CHANGE IT
FQDN_DOMAINS_LIST = []  # here test 256 domain names

WANTED_RESULT_DICT = {
    "valid": [],
    "invalid": []
}


def fn_timer(func):
    from functools import wraps

    @wraps(func)
    def function_timer(*args, **kwargs):
        import time
        time_begin = time.time()
        result = func(*args, **kwargs)
        time_end = time.time()
        print("Total time running {function_name}: {time_spent} seconds".format(function_name=func.__name__,
                                                                                time_spent=(time_end - time_begin)))

        return result

    return function_timer


def is_valid_fqdn_domain(domain):
    res = ping3.ping(dest_addr=domain, timeout=2)
    if res:
        return True
    else:
        return False


def check_domains_status():
    pass


def check_domain_status(domain):
    res = is_valid_fqdn_domain(domain)
    if res:
        return True, domain
    else:
        return False, domain


@fn_timer
def unoptimized_task():
    for name in FQDN_DOMAINS_LIST:
        res = is_valid_fqdn_domain(name)
        if res:
            WANTED_RESULT_DICT['valid'].append(name)
        else:
            WANTED_RESULT_DICT['invalid'].append(name)

    return WANTED_RESULT_DICT


@fn_timer
def optimized_task_using_threading_pool():
    # about 10~12 times faster than unoptimized_task
    queue = Queue()

    def is_valid_fqdn_domain_thread(payload):
        is_valid, domain = check_domain_status(payload)
        if is_valid:
            queue.put((is_valid, domain))
        return domain

    pool = ThreadPool(200)
    res = pool.map(is_valid_fqdn_domain_thread, FQDN_DOMAINS_LIST)
    pool.close()
    pool.join()
    print(res)
    for _ in range(queue.qsize()):
        print(queue.get())


if __name__ == '__main__':
    optimized_task_using_threading_pool()
