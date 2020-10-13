#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created by PyCharm.
File Name:              LinuxBashShellScriptForOps:python-connect-redis.py
Version:                0.0.1
Author:                 dgden
Author Email:           dgdenterprise@gmail.com
URL:                    https://github.com/DingGuodong/LinuxBashShellScriptForOps
Download URL:           https://github.com/DingGuodong/LinuxBashShellScriptForOps/tarball/master
Create Date:            2020/10/12
Create Time:            17:30
Description:            Python client for Redis key-value store
Long Description:
References:             https://pypi.org/project/redis/
Prerequisites:          pip install redis
Development Status:     3 - Alpha, 5 - Production/Stable
Environment:            Console
Intended Audience:      System Administrators, Developers, End Users/Desktop
License:                Freeware, Freely Distributable
Natural Language:       English, Chinese (Simplified)
Operating System:       POSIX :: Linux, Microsoft :: Windows
Programming Language:   Python :: 3
Topic:                  Utilities
 """
from redis import Redis


class MyRedis(object):
    def __init__(self):
        self.redis = Redis(host='192.168.88.18', port=6379, password='password',
                           decode_responses=True,
                           charset='UTF-8', encoding='UTF-8')


if __name__ == '__main__':
    my_redis = MyRedis()

    # https://redis.io/commands/info
    redis_info = my_redis.redis.info(section='server')
    redis_version = redis_info.get("redis_version")
    print(redis_version)

    # another usage
    also_my_redis = Redis(host='192.168.88.18', port=6379, password='password',
                          decode_responses=True,
                          charset='UTF-8', encoding='UTF-8')
    redis_info = also_my_redis.info(section='server')
    redis_version = redis_info.get("redis_version")
    print(redis_version)
