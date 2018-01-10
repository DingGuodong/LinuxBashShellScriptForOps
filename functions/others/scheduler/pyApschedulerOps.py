#!/usr/bin/python
# encoding: utf-8
# -*- coding: utf8 -*-
"""
Created by PyCharm.
File Name:              LinuxBashShellScriptForOps:pyApschedulerOps.py
Version:                0.0.1
Author:                 Guodong
Author Email:           dgdenterprise@gmail.com
URL:                    https://github.com/DingGuodong/LinuxBashShellScriptForOps
Download URL:           https://github.com/DingGuodong/LinuxBashShellScriptForOps/tarball/master
Create Date:            2018/1/10
Create Time:            13:43
Description:            Advanced Python Scheduler
Long Description:       
References:             https://apscheduler.readthedocs.io/en/latest/
Prerequisites:          pip install apscheduler
                        pip install sqlalchemy
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

import logging.handlers
import os
import sys
import time

from apscheduler.schedulers.background import BackgroundScheduler


def func_as_task_to_do():
    import time
    import arrow

    log_name = os.path.splitext(os.path.basename(__file__))[0]
    log_filename = log_name + ".log"
    log_file_max_size = 104857600  # 100MB
    log_file_save_number = 10  # save 10 log file
    log_file_path = os.path.abspath(os.path.join(os.path.curdir, log_filename))
    log_file_encoding = 'utf-8'
    log_formatter = logging.Formatter(fmt="%(asctime)s %(filename)s:%(lineno)d %(name)s %(levelname)s: %(message)s",
                                      datefmt=None)  # datefmt=None means "%Y-%m-%d %H:%M:%S" with %03d msecs, \
    # such as 2017-11-16 14:40:17,555

    file_handler = logging.handlers.RotatingFileHandler(log_file_path, maxBytes=log_file_max_size,
                                                        backupCount=log_file_save_number,
                                                        encoding=log_file_encoding)
    file_handler.setFormatter(log_formatter)
    stream_handler = logging.StreamHandler(sys.stderr)

    logger = logging.getLogger(log_name)
    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)
    logger.setLevel(logging.DEBUG)

    now = arrow.now('Asia/Shanghai').format()
    # after open log file, you will see there are only 3 logs records in this file within 60 seconds
    logger.info(now)
    time.sleep(60)

    return True


# Enable debug for apscheduler
logging.basicConfig()
logging.getLogger('apscheduler').setLevel(logging.DEBUG)

# Job setting
job_defaults = {
    'coalesce': False,
    # Execution of job skipped: maximum number of running instances reached (8)
    'max_instances': 8
}

scheduler = BackgroundScheduler(job_defaults=job_defaults)

job = scheduler.add_job(func_as_task_to_do, 'interval', seconds=1)
scheduler.print_jobs()
scheduler.start()

# Because of the scheduler is background scheduler not blocking scheduler, so we use a endless loop
print('Press Ctrl + {key} to exit.'.format(key='Break' if os.name == 'nt' else 'C'))
try:
    while True:
        time.sleep(2)
except (KeyboardInterrupt, SystemExit):
    # Not strictly necessary if daemonic mode is enabled but should be done if possible
    scheduler.shutdown()
    print('Exit now!')
