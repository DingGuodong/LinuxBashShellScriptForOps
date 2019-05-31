#!/usr/bin/python
# encoding: utf-8
# -*- coding: utf8 -*-
"""
Created by PyCharm.
File:               LinuxBashShellScriptForOps:pyMemcachedOps.py
User:               Guodong
Create Date:        2016/12/1
Create Time:        10:59


pip install --upgrade pip
pip install python-memcached

"""
import memcache

mc = memcache.Client(['memcached:11211'], debug=0)
mc.set("foo", "bar")
value = mc.get("foo")
if value == "bar":
    print("connect to memcached successfully!")
else:
    print("can NOT connect to memcached, failed!")
