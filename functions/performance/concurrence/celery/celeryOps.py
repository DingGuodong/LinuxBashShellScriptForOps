#!/usr/bin/python
# encoding: utf-8
# -*- coding: utf8 -*-
"""
Created by PyCharm.
File:               LinuxBashShellScriptForOps:celeryOps.py
User:               Guodong
Create Date:        2017/1/13
Create Time:        18:14
 """

from celery import Celery
import time

# redis://:password@hostname:port/db_number
# transport://userid:password@hostname:port/virtual_host

broker = 'amqp://rabbit:rabbitmq@10.20.0.129:5672//'
backend = 'redis://10.20.0.129:6379/0'
celery = Celery('tasks', broker=broker, backend=backend)


@celery.task
def sendmail(mail):
    print('sending mail to %s...' % mail['to'])
    time.sleep(2.0)
    print('mail sent.')
