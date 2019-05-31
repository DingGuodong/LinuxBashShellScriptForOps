#!/usr/bin/python
# encoding: utf-8
# -*- coding: utf8 -*-
"""
Created by PyCharm.
File Name:              LinuxBashShellScriptForOps:pySampleLogging.py
Version:                0.0.1
Author:                 Guodong
Author Email:           dgdenterprise@gmail.com
URL:                    https://github.com/DingGuodong/LinuxBashShellScriptForOps
Download URL:           https://github.com/DingGuodong/LinuxBashShellScriptForOps/tarball/master
Create Date:            2017/11/16
Create Time:            14:21
Description:            most sample logger function
Long Description:       
References:             
Prerequisites:          []
Development Status:     3 - Alpha, 5 - Production/Stable
Environment:            Console
Intended Audience:      System Administrators, Developers, End Users/Desktop
License:                Freeware, Freely Distributable
Natural Language:       English, Chinese (Simplified)
Operating System:       POSIX :: Linux, Microsoft :: Windows
Programming Language:   Python :: 3
Topic:                  Utilities
 """
import logging.handlers
import os
import sys
import time

log_name = "sample"
log_filename = "sample.log"
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

logger.info("test info")
time.sleep(0.1)  # in float, min unit: subsecond precision(<1.0s)
logger.error("test error")
logger.error(u"中国汉字")  # chinese language must in unicode
logger.error("中国汉字")
