#!/usr/bin/python
# encoding: utf-8
# -*- coding: utf8 -*-
"""
Created by PyCharm.
File:               LinuxBashShellScriptForOps:pyLogging_u1.py
User:               Guodong
Create Date:        2017/3/9
Create Time:        10:16

Upgrade Notes:
    updated from pyLogging.py

 """
import time
import os
import logging
import logging.handlers
import sys


def initLoggerWithRotate(logPath="/var/log", logName=None, singleLogFile=True):
    current_time = time.strftime("%Y%m%d%H")
    logRootPath = logPath  # logRootPath known as logTopPath
    if logName is not None and not singleLogFile:
        logFullPath = os.path.join(logRootPath, logName)
        logFilename = logName + "_" + current_time + ".log"
    elif logName is not None and singleLogFile:
        logFullPath = os.path.join(logRootPath, logName)
        logFilename = logName + ".log"
    else:
        logFullPath = logRootPath
        logName = "default"
        logFilename = logName + ".log"

    if not os.path.exists(logFullPath):
        os.makedirs(logFullPath)
        logFilename = os.path.join(logFullPath, logFilename)
    else:
        logFilename = os.path.join(logFullPath, logFilename)

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


if __name__ == '__main__':
    log_path = "/var/log"
    log_name = "." + os.path.splitext(os.path.basename(__file__))[0]

    log = initLoggerWithRotate(logPath="/var/log", logName=log_name, singleLogFile=True)
    log.setLevel(logging.INFO)
    log.info("if you can see this message, it means success")
