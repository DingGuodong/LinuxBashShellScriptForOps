#!/usr/bin/python
# encoding: utf-8
# -*- coding: utf8 -*-
"""
Created by PyCharm.
File:               LinuxBashShellScriptForOps:pythonLogging.py
User:               Guodong
Create Date:        2016/9/5
Create Time:        11:06
 """

import logging
import logging.handlers
import os
import time
import sys


def initLoggerWithRotate(logPath="/var/log", logName=None):
    current_time = time.strftime("%Y%m%d%H")
    if logName is not None:
        logPath = os.path.join(logPath, logName)
        logFilename = logName + "_" + current_time + ".log"
    else:
        logName = "default"
        logFilename = logName + ".log"

    if not os.path.exists(logPath):
        os.makedirs(logPath)
        logFilename = os.path.join(logPath, logFilename)
    else:
        logFilename = os.path.join(logPath, logFilename)

    logger = logging.getLogger(logName)
    log_formatter = logging.Formatter("%(asctime)s %(filename)s:%(lineno)d %(name)s %(levelname)s: %(message)s",
                                      "%Y-%m-%d %H:%M:%S")
    file_handler = logging.handlers.RotatingFileHandler(logFilename, maxBytes=104857600, backupCount=5)
    file_handler.setFormatter(log_formatter)
    stream_handler = logging.StreamHandler(sys.stderr)
    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)
    logger.setLevel(logging.DEBUG)
    return logger


MyLogger = initLoggerWithRotate("/var/log", "app_name")
# MyLogger.setLevel(logging.INFO)
MyLogger.debug("test logger, debug msg")
MyLogger.info("test logger, info msg")
