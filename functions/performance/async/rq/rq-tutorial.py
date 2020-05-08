#!/usr/bin/python
# encoding: utf-8
# -*- coding: utf8 -*-
"""
Created by PyCharm.
File Name:              LinuxBashShellScriptForOps:rq-tutorial.py
Version:                0.0.1
Author:                 Guodong
Author Email:           dgdenterprise@gmail.com
URL:                    https://github.com/DingGuodong/LinuxBashShellScriptForOps
Download URL:           https://github.com/DingGuodong/LinuxBashShellScriptForOps/tarball/master
Create Date:            2018/2/2
Create Time:            9:45
Description:            
Long Description:       
References:             http://python-rq.org/docs/
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

from redis import Redis
from rq import Worker, Queue, Connection

conn = Redis(host='localhost', port=6379, db=0, password=None)
q = Queue('default', connection=conn)

# use len() as a task(job)
job = q.enqueue(len, 'http://nvie.com')

# Limitations
# RQ workers will only run on systems that implement fork().
# Most notably, this means it is not possible to run the workers on Windows.
listen = ['default']
with Connection(conn):
    worker = Worker(list(map(Queue, listen)))
    worker.work()
