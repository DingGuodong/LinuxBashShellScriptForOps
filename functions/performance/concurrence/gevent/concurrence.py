#!/usr/bin/python
# encoding: utf-8
# -*- coding: utf8 -*-
"""
Created by PyCharm.
File:               LinuxBashShellScriptForOps:concurrence.py
User:               Guodong
Create Date:        2016/10/14
Create Time:        10:59
"""

#  execute some operations concurrently using python
from gevent import monkey

monkey.patch_all()
import gevent
import urllib2


def f(url):
    print('GET: %s' % url)
    resp = urllib2.urlopen(url)
    data = resp.read()
    print('%d bytes received from %s.' % (len(data), url))


hosts = ['https://www.python.org/', 'https://github.com/', 'http://weixin.qq.com/']

gevent.joinall([gevent.spawn(f, host) for host in hosts])
