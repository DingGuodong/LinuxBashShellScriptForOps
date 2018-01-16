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
import shutil
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


def decoding(text):
    import sys
    import codecs
    import locale

    if isinstance(text, unicode):
        return text
    elif isinstance(text, (basestring, str)):
        pass
    else:
        return text  # do not need decode, return original object if type is not instance of string type
        # raise RuntimeError("expected type is str, but got {type} type".format(type=type(text)))

    mswindows = (sys.platform == "win32")

    try:
        encoding = locale.getdefaultlocale()[1] or ('ascii' if not mswindows else 'gbk')
        codecs.lookup(encoding)  # codecs.lookup('cp936').name == 'gbk'
    except Exception as _:
        del _
        encoding = 'ascii' if not mswindows else 'gbk'  # 'gbk' is Windows default encoding in Chinese language 'zh-CN'

    msg = text
    if mswindows:
        try:
            msg = text.decode(encoding)
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

    # clean old backups, and save 3 copies
    save_backups = 3  # save 3 copies
    all_backups = list()
    if len(os.listdir(backup_storage)) > save_backups:
        log.info("old backups are found, ready to remove.")
        for copy in os.listdir(backup_storage):
            if copy.startswith('bak20'):  # bug fixed, but a regular expression maybe best choice
                all_backups.append(copy)


        def compare_by_time(x, y):
            # compare two files by their time of last change
            stat_x = os.stat(os.path.join(backup_storage, x))
            stat_y = os.stat(os.path.join(backup_storage, y))
            # if stat_x.st_ctime < stat_y.st_ctime:  # time of last change
            #     return -1
            # elif stat_x.st_ctime > stat_y.st_ctime:
            #     return 1
            # else:
            #     return 0
            return cmp(stat_x.st_ctime, stat_y.st_ctime)


        all_backups.sort(compare_by_time)  # sort files in dir by time

        valid_backups_copies = all_backups[-save_backups:]
        for copy in all_backups:
            if copy not in valid_backups_copies:
                old_backup = os.path.join(backup_storage, copy)
                shutil.rmtree(old_backup)
                log.info("  old backup %s is removed" % old_backup)

    end_time = time.time()
    log.info("=" * 16 + "backup finished." + "=" * 16)
    log.info("State:      %s." % ("Success" if is_success else "Failed"))
    log.info("Start time: %s" % time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(start_time)))
    log.info("End time:   %s" % time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(end_time)))
    log.info("Spent time: using %d seconds." % (end_time - start_time))
    log.info("=" * 64 + "\n" * 2)
