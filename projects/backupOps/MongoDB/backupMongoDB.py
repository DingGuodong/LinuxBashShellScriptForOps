#!/usr/bin/python
# encoding: utf-8
# -*- coding: utf8 -*-
"""
Created by PyCharm.
File:               LinuxBashShellScriptForOps:backupMongoDB.py
User:               Guodong
Create Date:        2017/9/21
Create Time:        14:20
Description:        python script for backup MongoDB databases
References:         
Prerequisites:      []
 """
import logging
import logging.handlers
import os
import subprocess
import sys
import time
from collections import Iterable


def initLoggerWithRotate(logPath="/var/log", logName=None, singleLogFile=True):
    current_time = time.strftime("%Y%m%d%H")
    if logName is not None and not singleLogFile:
        logPath = os.path.join(logPath, logName)
        logFilename = logName + "_" + current_time + ".log"
    elif logName is not None and singleLogFile:
        logPath = os.path.join(logPath, logName)
        logFilename = logName + ".log"
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


def get_system_encoding():
    """
    The encoding of the default system locale but falls back to the given
    fallback encoding if the encoding is unsupported by python or could
    not be determined.  See tickets #10335 and #5846
    """
    import codecs
    import locale
    import sys
    mswindows = (sys.platform == "win32")
    try:
        encoding = locale.getdefaultlocale()[1] or ('ascii' if not mswindows else 'gbk')
        codecs.lookup(encoding)
    except Exception as e:
        del e
        encoding = 'ascii' if not mswindows else 'gbk'  # 'gbk' is Windows default encoding in Chinese language 'zh-CN'
    return encoding


DEFAULT_LOCALE_ENCODING = get_system_encoding()


def decoding(text):
    import sys

    mswindows = (sys.platform == "win32")

    msg = text
    if mswindows:
        try:
            msg = text.decode(DEFAULT_LOCALE_ENCODING)
            return msg
        except (UnicodeDecodeError, UnicodeEncodeError):
            pass
    return msg


if __name__ == '__main__':
    now = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    task_name = 'backup_mongodb'
    backup_storage = r'D:\DbBak'
    backup_dir = "bak" + time.strftime('%Y-%m-%d', time.localtime(time.time()))

    mongodb_host = 'localhost'
    mongodb_port = '28188'
    mongodb_database = 'usertrack'
    mongodb_bin_dump = r'"C:\Program Files\MongoDB\bin\mongodump.exe"'

    backup_cmd = '{mongodump} --host {host} --port {port} --db {database} --out {out}'.format(
        mongodump=mongodb_bin_dump,
        host=mongodb_host,
        port=mongodb_port,
        database=mongodb_database,
        out=os.path.join(backup_storage, backup_dir)
    )

    log = initLoggerWithRotate(logPath=backup_storage, logName=task_name, singleLogFile=True)
    log.setLevel(logging.INFO)

    log.info(">" * 16 + "backup started." + ">" * 16)
    start_time = time.time()
    is_success = False
    try:
        p = subprocess.Popen(backup_cmd, shell=True, stdout=subprocess.PIPE,
                             stderr=subprocess.STDOUT)
        (stdout, stderr) = p.communicate()

        if p.returncode != 0:
            log.error("encountered an error (return code %s) while executing '%s'" % (p.returncode, backup_cmd))
            if stdout is not None:
                log.error(decoding("Standard output: " + stdout))
            if stderr is not None:
                log.error(decoding("Standard error: " + stderr))
        else:
            is_success = True
            if stdout is not None:
                log.info(decoding(stdout))
    except Exception as exc:
        now = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        log.error("We encountered an exception at %s, Errors message as follow:" % now)
        # send mail to sysadmin etc.
        log.error(exc)
        if isinstance(exc, Iterable):
            for message in exc:
                log.error(message)
        for message in exc.args:
            log.error(message)

        for message in exc.message:
            log.error(message)
        log.error("=" * 64)
        sys.exit(1)

    end_time = time.time()
    log.info("=" * 16 + "backup finished." + "=" * 16)
    log.info("State:      %s." % ("Success" if is_success else "Failed"))
    log.info("Start time: %s" % time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(start_time)))
    log.info("End time:   %s" % time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(end_time)))
    log.info("Spent time: using %d seconds." % (end_time - start_time))
    log.info("=" * 64 + "\n" * 2)
