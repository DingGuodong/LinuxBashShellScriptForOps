#!/usr/bin/python
# encoding: utf-8
# -*- coding: utf8 -*-
"""
Created by PyCharm.
File:               LinuxBashShellScriptForOps:pyConnectRabbitmq.py
User:               Guodong
Create Date:        2016/12/7
Create Time:        15:02
 """
import pika
import sys

parameters = pika.URLParameters('amqp://guest:guest@10.6.28.36:5672/%2F?backpressure_detection=t')
connection = None
try:
    connection = pika.BlockingConnection(parameters)
except Exception as e:
    if e.message:
        print e.message
finally:
    if connection:
        print "connect to rabbitmq successfully"
    else:
        print "cannot connect to rabbitmq"
        sys.exit(1)
