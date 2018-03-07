#!/usr/bin/python
# encoding: utf-8
# -*- coding: utf8 -*-
"""
Created by PyCharm.
File Name:              LinuxBashShellScriptForOps:pyRedisConnectivityQuickTest.py
Version:                0.0.1
Author:                 Guodong
Author Email:           dgdenterprise@gmail.com
URL:                    https://github.com/DingGuodong/LinuxBashShellScriptForOps
Download URL:           https://github.com/DingGuodong/LinuxBashShellScriptForOps/tarball/master
Create Date:            2018/3/6
Create Time:            16:45
Description:            Python Redis Connectivity Quick Test
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

import redis


def redis_conn_qt(host, port, db=0, password=None, show_reason=False):
    try:
        client = redis.StrictRedis(host, port, db, password, socket_connect_timeout=5)
    except redis.exceptions.ConnectionError as e:
        if show_reason:
            print("ConnectionError 1")
            print(e)
            print(e.args)
        return False

    if client:
        try:
            client.set("6d78247b460acc6bf1d9263e14382fea", "1")
        except redis.exceptions.ConnectionError as e:
            if show_reason:
                print("ConnectionError 2")
                print(e)
                print(e.args)
            return False
        except redis.exceptions.ResponseError as e:
            if show_reason:
                print("ResponseError")
                print(e)
                print(e.args)
            return False

    return True


if __name__ == '__main__':
    redis_host = "127.0.0.1"
    redis_port = 6379
    redis_password = ""
    print(redis_conn_qt(redis_host, redis_port, password=redis_password, show_reason=True))
