#!/usr/bin/python
# encoding: utf-8
# -*- coding: utf8 -*-
"""
Created by PyCharm.
File:               LinuxBashShellScriptForOps:pyRedisOps.py
User:               Guodong
Create Date:        2016/9/7
Create Time:        10:36

Redis client basic operations

 """

import redis

redis_host = "127.0.0.1"
redis_port = 6379
redis_password = ""

try:
    c = redis.StrictRedis(host=redis_host, port=redis_port, password=redis_password, socket_timeout=5)
    role = c.info().get('role')
    if not c.exists('redis_role_status') or c.get('redis_role_status') != role:
        c.set('redis_role_status', role)
    print(c.get('redis_role_status'))
except (redis.exceptions.ConnectionError, redis.exceptions.TimeoutError, redis.exceptions.ResponseError) as e:
    print(e)
