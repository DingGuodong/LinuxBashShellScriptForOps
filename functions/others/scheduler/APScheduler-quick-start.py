#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created by PyCharm.
File Name:              LinuxBashShellScriptForOps:APScheduler-quick-start.py
Version:                0.0.1
Author:                 Guodong
Author Email:           dgdenterprise@gmail.com
URL:                    https://github.com/DingGuodong/LinuxBashShellScriptForOps
Download URL:           https://github.com/DingGuodong/LinuxBashShellScriptForOps/tarball/master
Create Date:            2019/5/20
Create Time:            12:04
Description:            APScheduler quick start and examples
Long Description:       
References:             https://github.com/agronholm/apscheduler/tree/master/examples
Prerequisites:          pip install APScheduler
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

import logging
import os
from datetime import datetime
from logging.handlers import TimedRotatingFileHandler

from apscheduler.events import EVENT_JOB_EXECUTED, EVENT_JOB_ERROR
from apscheduler.schedulers.blocking import BlockingScheduler

logger = logging.getLogger('mylog')


def set_file_logger_date(filename, name="mylog", saves=10, level=logging.INFO, format_string=None):
    global logger
    if not format_string:
        format_string = "%(asctime)s %(name)s %(levelname)s %(thread)d : %(message)s"
    logger = logging.getLogger(name)
    logger.setLevel(level)
    file_handler = TimedRotatingFileHandler(filename, when='d', backupCount=saves, )
    file_handler.setLevel(level)
    formatter = logging.Formatter(format_string, datefmt=None)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)


def set_stream_logger(name='mylog', level=logging.DEBUG, format_string=None):
    """
    stream logger for debug purpose
    """
    global logger
    if not format_string:
        format_string = "%(asctime)s %(name)s %(levelname)s %(pathname)s:%(lineno)d " \
                        "%(process)d %(thread)d : %(message)s"  # see logging.__init__.Formatter()
    logger = logging.getLogger(name)
    logger.setLevel(level)
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(level)
    formatter = logging.Formatter(format_string, datefmt=None)  # the ISO8601 date format, 2018-12-11 15:01:17,290
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)


set_stream_logger('mylog', logging.INFO)


def tick():
    print('Tick! The time is: %s' % datetime.now())


def interval_example1():
    """
    Demonstrates how to schedule a job to be run in a process pool on 3 second intervals.
    """
    scheduler = BlockingScheduler()
    scheduler.add_executor('processpool')
    scheduler.add_job(tick, 'interval', seconds=3)
    print('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))

    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        pass


def interval_example2():
    """
    Basic example showing how to schedule a callable using a textual reference.
    """
    scheduler = BlockingScheduler()
    scheduler.add_job('sys:stdout.write', 'interval', seconds=3, args=['tick\n'])
    print('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))

    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        pass


def cron_example1():
    scheduler = BlockingScheduler()
    scheduler.add_job('sys:stdout.write', 'cron', year=2019, month=5, day=20, hour=18, minute=26, second=1,
                      args=['tick\n'])
    print('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))

    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        pass


def cron_example2():
    scheduler = BlockingScheduler()
    scheduler.add_job('sys:stdout.write', 'cron', day_of_week='mon-fri', hour=19, minute=30, end_date='2020-05-20',
                      args=['tick\n'])
    print('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))

    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        pass


def event_listener(event):
    if event.exception:
        print 'exception'
    else:
        print 'continue'


def date_example1():
    scheduler = BlockingScheduler()
    scheduler.add_job('sys:stdout.write', 'date', run_date=datetime(2019, 05, 20, 18, 54),
                      args=['tick\n'])
    print('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))

    scheduler.add_listener(event_listener, EVENT_JOB_EXECUTED | EVENT_JOB_ERROR)
    scheduler._logger = logger

    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        pass


if __name__ == '__main__':
    date_example1()
