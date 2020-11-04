#!/usr/bin/python
# encoding: utf-8
# -*- coding: utf-8 -*-
"""
Created by PyCharm.
File Name:              LinuxBashShellScriptForOps:pyLogging_u4.py.py
Version:                0.0.1
Author:                 Guodong
Author Email:           dgdenterprise@gmail.com
URL:                    https://github.com/DingGuodong/LinuxBashShellScriptForOps
Download URL:           https://github.com/DingGuodong/LinuxBashShellScriptForOps/tarball/master
Create Date:            2020/11/04
Create Time:            10:35
Description:            better logging support for large project
Long Description:       we can add this part of code into __init__.py for project
References:             
Prerequisites:          []
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

import os

import logging
from logging.handlers import TimedRotatingFileHandler

logger = logging.getLogger()


def set_logger(filename, name="root", saves=10, level=logging.INFO, format_string=None):
    if not format_string:
        format_string = "%(asctime)s %(name)s %(levelname)7s %(thread)d: %(message)s"
    logger.name = name
    logger.setLevel(level)

    file_handler = TimedRotatingFileHandler(filename, when='d', backupCount=saves, )
    file_handler.setLevel(level)

    # also send message to sys.stderr
    stream_handler = logging.StreamHandler(stream=None)
    stream_handler.setLevel(level)

    formatter = logging.Formatter(format_string, datefmt=None)
    file_handler.setFormatter(formatter)
    stream_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)


def console_log_msg(msg, level="info", name="root"):
    """
    send log to file and sys.stderr
    :param msg: str, log message
    :param level: str, log severity, error、warn、debug、info
    :param name: str, set the logger with the specified name
    :return:
    """
    if not logger.handlers:  # block same/duplicate Log messages/entries multiple times
        set_logger(self_script_output_log_path, name=name, level=logging.DEBUG)

    logger.name = name

    level = level.lower()

    if level == "error" or "err" in level:
        logger.error(msg)
    elif "warn" in level:
        logger.warning(msg)
    elif "debug" in level:
        logger.debug(msg)
    else:
        logger.info(msg)


if __name__ == '__main__':
    self_script_output_log_path = r"./{}.log".format(os.path.basename(__file__))

    console_log_msg("some msg here")

    # using unicode or str with 'utf-8' for non-ascii character
    console_log_msg(u"打印一些日志")
    console_log_msg("打印一些日志".decode('utf-8'))  # 'utf-8' same with '-*- coding: utf-8 -*-', they must be same

    console_log_msg("这是一条错误信息", level="error", name="hello")
    console_log_msg("这是一条警告信息", "warn")
