#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created by PyCharm.
File Name:              LinuxBashShellScriptForOps:pyKafkaOps.py
Version:                0.0.1
Author:                 dgden
Author Email:           dgdenterprise@gmail.com
URL:                    https://github.com/DingGuodong/LinuxBashShellScriptForOps
Download URL:           https://github.com/DingGuodong/LinuxBashShellScriptForOps/tarball/master
Create Date:            2019/11/14
Create Time:            13:53
Description:            
Long Description:       
References:             https://github.com/dpkp/kafka-python
                        https://kafka-python.readthedocs.io/en/master/
Prerequisites:          pip2.7 install kafka-python
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
# from multiprocessing import pool
import json

from kafka import KafkaProducer, KafkaConsumer


# https://github.com/dpkp/kafka-python#kafkaproducer
# Tips:
# if you want to access kafka on the Internet rather than local or Intranet(Internal network),
# you need configure 'advertised.listeners=PLAINTEXT://<public ip>:9092' in 'config/server.properties',
# even if you have no public ip displayed on system but you can access system with that public ip.

def kafka_producer_test():
    # https://github.com/dpkp/kafka-python#kafkaconsumer
    producer = KafkaProducer(
        bootstrap_servers=['172.26.210.149:9092', '172.26.210.150:9092', '172.26.210.151:9092'],
        value_serializer=lambda v: json.dumps(v).encode('utf-8')
    )

    future = producer.send(topic='service_test', value={'foo': 'bar'})
    result = future.get(timeout=60)
    print(result)

    metrics = producer.metrics()
    print(metrics)


def kafka_consumer_test():
    consumer = KafkaConsumer("service_test",
                             bootstrap_servers=['172.26.210.149:9092', '172.26.210.150:9092', '172.26.210.151:9092'],
                             )
    # blocked and waiting for producer send msg,
    # refer to: consumer.next(), consumer.__next__(), next(consumer)
    # impl: next + while + yield
    for msg in consumer:
        print msg, msg.value
