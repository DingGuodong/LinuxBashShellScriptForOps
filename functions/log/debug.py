#!/usr/bin/python
# encoding: utf-8
# -*- coding: utf8 -*-
"""
Created by PyCharm.
File:               LinuxBashShellScriptForOps:debug.py
User:               Guodong
Create Date:        2016/11/8
Create Time:        11:46
 """
import os
import sys
import time
import logging
import logging.handlers


class debug(object):
    def __init__(self):
        self.name = None

    def log(self, name=None, path=None):
        if name is not None:
            self.name = name
        else:
            self.name = 'default'

        if path is not None and os.path.exists(path):
            logpath = path
        else:
            logpath = "/tmp"
        current_time = time.strftime("%Y%m%d%H")
        logfile = self.name + current_time + ".log"
        if not os.path.exists(logpath):
            os.makedirs(logpath)
        else:
            logfile = os.path.join(logpath, logfile)

        logger = logging.getLogger(name=self.name)
        log_formatter = logging.Formatter("%(asctime)s %(filename)s:%(lineno)d %(name)s %(levelname)s: %(message)s",
                                          "%Y-%m-%d %H:%M:%S")
        file_handler = logging.handlers.RotatingFileHandler(logfile, maxBytes=104857600, backupCount=5)
        file_handler.setFormatter(log_formatter)
        stream_handler = logging.StreamHandler(sys.stderr)
        logger.addHandler(file_handler)
        logger.addHandler(stream_handler)
        logger.setLevel(logging.DEBUG)
        return logger


log = debug()
