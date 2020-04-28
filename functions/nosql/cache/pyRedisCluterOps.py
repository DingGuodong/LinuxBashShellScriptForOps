#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created by PyCharm.
File Name:              LinuxBashShellScriptForOps:pyRedisCluterOps.py
Version:                0.0.1
Author:                 dgden
Author Email:           dgdenterprise@gmail.com
URL:                    https://github.com/DingGuodong/LinuxBashShellScriptForOps
Download URL:           https://github.com/DingGuodong/LinuxBashShellScriptForOps/tarball/master
Create Date:            2019/11/14
Create Time:            11:52
Description:            Redis Cluster Client for Python
Long Description:       
References:             [Redis cluster tutorial](https://redis.io/topics/cluster-tutorial)
Prerequisites:          pip install redis-py-cluster
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
from rediscluster import RedisCluster

# Requires at least one node for cluster discovery. Multiple nodes is recommended.
startup_nodes = [
    {"host": "172.26.109.195", "port": "6379"},
    {"host": "172.26.109.194", "port": "6379"},
    {"host": "172.26.109.193", "port": "6379"},
    {"host": "172.26.109.195", "port": "6380"},
    {"host": "172.26.109.194", "port": "6380"},
    {"host": "172.26.109.193", "port": "6380"},
]

rc = RedisCluster(startup_nodes=startup_nodes, decode_responses=True, socket_timeout=2)
rc.set("foo", "bar")
print(rc.get("foo"))
