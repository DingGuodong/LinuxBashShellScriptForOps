#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created by PyCharm.
File Name:              LinuxBashShellScriptForOps:redis-performance-tester.py
Version:                0.0.1
Author:                 dgden
Author Email:           dgdenterprise@gmail.com
URL:                    https://github.com/DingGuodong/LinuxBashShellScriptForOps
Download URL:           https://github.com/DingGuodong/LinuxBashShellScriptForOps/tarball/master
Create Date:            2021/3/25
Create Time:            14:28
Description:            do a performance benchmark for redis-server using python and redis library
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
import warnings

from redis import Redis

redis_conn = Redis(host='127.0.0.1', port=6379, password='',
                   decode_responses=True,
                   charset='UTF-8', encoding='UTF-8')
redis_info = redis_conn.info(section='server')
redis_version = redis_info.get("redis_version")
print("redis_version:{}".format(redis_version))


def _do_redis_benchmark():
    # redis-benchmark -c 1 -n 10000 incr x 1
    test_key_name = "x"
    redis_conn.delete(test_key_name)
    start_time = time.time()
    while True:
        redis_conn.incr(test_key_name, 1)
        spent_time = time.time() - start_time
        if spent_time >= 1.0:
            break
    count = redis_conn.get("x")
    precise_count = float(count) / spent_time

    return precise_count


def do_redis_benchmark(times=4):
    benchmark_result = [_do_redis_benchmark() for _ in range(times)]
    max_count = max(benchmark_result)
    min_count = min(benchmark_result)
    avg_count = sum(benchmark_result) / times
    print("do {times} times bench(using redis `INCR`), max: {max}, min: {min}, avg: {avg} requests per second".format(
        times=times,
        max=max_count,
        min=min_count,
        avg=avg_count))


if __name__ == '__main__':
    warnings.warn("Tips: you can use `redis-benchmark` to test full performance of Redis server.")
    do_redis_benchmark()
