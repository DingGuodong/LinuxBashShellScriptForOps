#!/usr/bin/python
# encoding: utf-8
# -*- coding: utf8 -*-
"""
Created by PyCharm.
File:               LinuxBashShellScriptForOps:pyRedisOps.py
User:               Guodong
Create Date:        2016/9/7
Create Time:        10:36
 """

import redis

redis_host = "10.6.28.46"
redis_port = 6379
redis_password = "6d78247b460acc6bf1d9263e14382fea"

c = redis.StrictRedis(host=redis_host, port=redis_port, password=redis_password)
c.set("a", "1")
c.set("a", "2", nx=True)
print c.get("a")
