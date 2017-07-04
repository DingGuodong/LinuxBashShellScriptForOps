#!/usr/bin/python
# encoding: utf-8
# -*- coding: utf8 -*-
"""
Created by PyCharm.
File:               LinuxBashShellScriptForOps:backup-addc.py
User:               Guodong
Create Date:        2017/5/8
Create Time:        18:56

Function:
    copy files from 'Windows Server Backup' to remote NAS server, mount NAS server to Z: using a network driver
    save 2 copies
 """
import os
import sys
import shutil
import hashlib
import logging
import logging.handlers
import time

task_name = 'wsbh'  # task name will be used in log filename, connect words with underline '_', such as 'good_name'
# 'wsbh' is short for 'Windows Server Backup Helper'
backup_source = r"F:\WindowsImageBackup"  # do NOT end with backslash '\'.
backup_target = r'Z:\Server_Backup\VM-DC2'  # please using abs path here, and do NOT end with backslash '\'.
validate = False  # using validate will require more long time, set validate to False to improve performance
retry_times = 3


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


BackupLogger = initLoggerWithRotate(logPath="/var/log", logName=".backup_" + task_name, singleLogFile=True)
BackupLogger.setLevel(logging.INFO)


def get_hash_sum(FILE, method="md5", block_size=65536):
    if not os.path.exists(FILE):
        raise RuntimeError("cannot open '%s' (No such file or directory)" % FILE)
    if not os.path.isfile(FILE):
        raise RuntimeError("'%s' :not a regular file" % FILE)

    if "md5" in method:
        checksum = hashlib.md5()
    elif "sha1" in method:
        checksum = hashlib.sha1()
    elif "sha256" in method:
        checksum = hashlib.sha256()
    else:
        raise RuntimeError("unsupported method %s" % method)

    # if os.path.exists(filename) and os.path.isfile(filename):
    with open(FILE, 'rb') as f:
        buf = f.read(block_size)
        while len(buf) > 0:
            checksum.update(buf)
            buf = f.read(block_size)
        if checksum is not None:
            return checksum.hexdigest()
        else:
            return checksum


if os.path.exists(backup_source):
    pass
else:
    raise RuntimeError("'backup_source' is not exist!")

backup_source = os.path.abspath(backup_source)

start_time = time.time()

try:
    BackupLogger.info('backup files to remote filesystem')
    BackupLogger.info('>>>>>>>>>>>>>>>> Start >>>>>>>>>>>>>>>>')
    print 'Current time: {current_time}'.format(
        current_time=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))

    date_now = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
    if os.path.exists(backup_target):
        os.mkdir(os.path.join(backup_target, date_now))
    else:
        os.makedirs(os.path.join(backup_target, date_now))

    # clean old backups on remote target, save 2 copies
    if len(os.listdir(backup_target)) > 2:
        valid_backups_copies = os.listdir(backup_target)[-2:]
        for copy in os.listdir(backup_target):
            if copy not in valid_backups_copies:
                shutil.rmtree(os.path.join(backup_target, copy))
    backup_target = os.path.join(backup_target, date_now)
    for top, dirs, nondirs in os.walk(backup_source, followlinks=True):
        for directory in dirs:
            src_directory = os.path.abspath(os.path.join(top, directory))
            # print src_directory
            dst_directory = src_directory.replace(os.path.abspath(backup_source), backup_target)
            if not os.path.exists(dst_directory):
                os.makedirs(dst_directory)
        for filename in nondirs:
            src_filename = os.path.abspath(os.path.join(top, filename))
            # print src_filename
            dst_filename = src_filename.replace(os.path.abspath(backup_source), backup_target)
            if not os.path.exists(src_filename) or os.path.islink(src_filename):
                # very useful when source file comes from docker volume with a symbolic links
                # which not exists on host filesystem
                links_path = "%s -> %s" % (src_filename, os.readlink(src_filename))
                BackupLogger.error("> may be a symbolic links exception: %s" % links_path)
            if not os.path.exists(dst_filename) and os.path.exists(src_filename):
                shutil.copy2(src_filename, dst_filename)
                if validate:
                    # there can be using a hash list(*.csv, *.json, file) to improve performance,
                    # and it will be useful when using scp to remote host
                    while retry_times > 0:
                        src_hash = get_hash_sum(src_filename)
                        dst_hash = get_hash_sum(dst_filename)
                        if dst_hash != src_hash:
                            BackupLogger.error("Transfer error occurs, source file is: %s" % src_filename)
                            retry_times -= 1
                            if not os.path.exists(dst_filename) and os.path.exists(src_filename):
                                shutil.rmtree(dst_filename)
                            shutil.copy2(src_filename, dst_filename)
                        else:
                            break
    end_time = time.time()
    spent_time = end_time - start_time
    BackupLogger.info("Finished with %s seconds." % spent_time)
    BackupLogger.info('================ End ================')
except (KeyboardInterrupt, SystemExit) as e:
    if e:
        BackupLogger.error(e, exc_info=True)
    BackupLogger.error('================ Error ================')
    sys.exit(1)
except (OSError, IOError) as e:
    if e:
        BackupLogger.critical(e, exc_info=1)
    BackupLogger.error('================ Error ================')
    sys.exit(1)
