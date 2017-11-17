#!/usr/bin/python
# encoding: utf-8
# -*- coding: utf8 -*-
"""
Created by PyCharm.
File Name:              LinuxBashShellScriptForOps:pyFakeDaemon.py
Version:                0.0.1
Author:                 Guodong
Author Email:           dgdenterprise@gmail.com
URL:                    https://github.com/DingGuodong/LinuxBashShellScriptForOps
Download URL:           https://github.com/DingGuodong/LinuxBashShellScriptForOps/tarball/master
Create Date:            2017/11/17
Create Time:            10:12
Description:            a fake daemon can run in Linux or Windows for Test purpose written by Python
Long Description:       WTF: in fact I begin this task on 17:10 because of too many interrupt, :(
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
import logging.handlers
import os
import signal
import sys
import time

log_name = os.path.splitext(os.path.basename(__file__))[0]
log_filename = "%s.log" % log_name
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


def sigterm_handler(_signo, _stack_frame):
    # Raises SystemExit(0):
    global keep_running_flag
    keep_running_flag = False


def sigkill_handler(_signo, _stack_frame):
    logger.warning("Ops, not kill me, please, let me exit with safe")
    raise NotImplementedError


if __name__ == '__main__':
    signal.signal(signal.SIGTERM, sigterm_handler)

    try:
        keep_running_flag = True
        logger.info(
            "Hello, process \"{process}\" is in running state, and pid is {pid}.".format(process=sys.argv[0],
                                                                                         pid=os.getpid()))
        time_start = time.time()
        while keep_running_flag:
            # time_now = time.time()
            # logger.info("process has run {seconds} seconds".format(seconds=(time_now - time_start)))
            # logger.info("sleep 1 second again.")
            time.sleep(1)
        logger.warning("keep running flag changed into False, exit now")
        sys.exit(0)
    except SystemExit:
        # Signal     Value     Action   Comment
        # SIGTERM      15       Term    Termination signal
        logger.warning("caught SystemExit, exit now")
    except KeyboardInterrupt:
        # Signal     Value     Action   Comment
        # SIGINT        2       Term    Interrupt from keyboard
        logger.warning("caught KeyboardInterrupt, exit now")
    finally:
        time_now = time.time()
        logger.info("process has run {seconds} seconds".format(seconds=(time_now - time_start)))
        logger.warning("Oh, process enter into shutdown state, good bye")
        sys.exit(0)
