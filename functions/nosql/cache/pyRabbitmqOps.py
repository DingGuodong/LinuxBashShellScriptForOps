#!/usr/bin/python
# encoding: utf-8
# -*- coding: utf8 -*-
"""
Created by PyCharm.
File:               LinuxBashShellScriptForOps:pyRabbitmqOps.py
User:               Guodong
Create Date:        2017/1/13
Create Time:        14:24
 """
import pika
import sys

connection = pika.BlockingConnection(pika.ConnectionParameters(
    host='10.20.0.129', port=5672,
    credentials=pika.credentials.PlainCredentials(username="rabbit", password="rabbitmq")))
channel = connection.channel()

channel.queue_declare(queue='task_queue', durable=True)

message = ' '.join(sys.argv[1:]) or "Hello World!"
channel.basic_publish(exchange='',
                      routing_key='task_queue',
                      body=message,
                      properties=pika.BasicProperties(
                          delivery_mode=2,  # make message persistent
                      ))
print(" [x] Sent %r" % message)
connection.close()
