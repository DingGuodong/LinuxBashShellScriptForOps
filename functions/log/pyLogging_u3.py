#!/usr/bin/python
# encoding: utf-8
# -*- coding: utf-8 -*-
"""
Created by PyCharm.
File Name:              LinuxBashShellScriptForOps:pyLogging_u3.py
Version:                0.0.1
Author:                 Guodong
Author Email:           dgdenterprise@gmail.com
URL:                    https://github.com/DingGuodong/LinuxBashShellScriptForOps
Download URL:           https://github.com/DingGuodong/LinuxBashShellScriptForOps/tarball/master
Create Date:            2018/8/16
Create Time:            11:55
Description:            a simple logger class for python script use
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
import sys


class log:
    def __init__(self, name='root', path='/tmp/root.log'):
        max_size = 104857600
        save_number = 10
        encoding = 'utf-8'
        fmt = logging.Formatter(fmt="%(asctime)s %(name)s %(levelname)s: %(message)s", datefmt=None)

        file_handler = logging.handlers.RotatingFileHandler(path, maxBytes=max_size,
                                                            backupCount=save_number,
                                                            encoding=encoding)
        file_handler.setFormatter(fmt)
        stream_handler = logging.StreamHandler(sys.stderr)

        self.logger = logging.getLogger(name)
        self.logger.addHandler(file_handler)
        self.logger.addHandler(stream_handler)
        self.logger.setLevel(logging.DEBUG)

    def success(self, msg):
        self.info(msg)

    def failed(self, msg):
        self.logger.error(msg)

    def info(self, msg):
        self.logger.info(msg)

    def warning(self, msg):
        self.logger.warning(msg)

    def error(self, msg):
        self.logger.error(msg)

    def critical(self, msg):
        self.logger.critical(msg)

    def debug(self, msg):
        self.logger.debug(msg)


if __name__ == '__main__':
    show = log("mylogname", "/tmp/mylogname.log")
    show.success("success")
    show.failed("failed")
