#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created by PyCharm.
File Name:              LinuxBashShellScriptForOps:clean-old-backup-files.py
Version:                0.0.1
Author:                 dgden
Author Email:           dgdenterprise@gmail.com
URL:                    https://github.com/DingGuodong/LinuxBashShellScriptForOps
Download URL:           https://github.com/DingGuodong/LinuxBashShellScriptForOps/tarball/master
Create Date:            2020/2/17
Create Time:            16:58
Description:            delete old backups in a group of specified folder
Long Description:       in this case, this script will delete SQL Server backup files (*.bak)
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
import json
import os
import re
import sys
from collections import defaultdict

import logging
from logging.handlers import RotatingFileHandler, TimedRotatingFileHandler

DEBUG = False

logger = logging.getLogger('mylog')


def set_file_logger(filename, name="mylog", level=logging.INFO, format_string=None):
    global logger
    if not format_string:
        format_string = "%(asctime)s %(name)s %(levelname)s %(thread)d : %(message)s"
    logger = logging.getLogger(name)
    logger.setLevel(level)
    file_handler = logging.FileHandler(filename)
    file_handler.setLevel(level)
    formatter = logging.Formatter(format_string, datefmt=None)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)


def set_file_logger_date(filename, name="mylog", saves=10, level=logging.INFO, format_string=None):
    global logger
    if not format_string:
        format_string = "%(asctime)s %(name)s %(levelname)s %(thread)d : %(message)s"
    logger = logging.getLogger(name)
    logger.setLevel(level)
    file_handler = TimedRotatingFileHandler(filename, when='d', backupCount=saves, )
    file_handler.setLevel(level)
    formatter = logging.Formatter(format_string, datefmt=None)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)


def set_file_logger_size(filename, name="mylog", max_size=1024 * 1024 * 2, saves=10, level=logging.INFO,
                         format_string=None):
    global logger
    if not format_string:
        format_string = "%(asctime)s %(name)s %(levelname)s %(thread)d : %(message)s"
    logger = logging.getLogger(name)
    logger.setLevel(level)
    file_handler = RotatingFileHandler(filename, maxBytes=max_size, backupCount=saves)
    file_handler.setLevel(level)
    formatter = logging.Formatter(format_string, datefmt=None)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)


def set_stream_logger(name='mylog', level=logging.DEBUG, format_string=None):
    """
    stream logger for debug purpose
    """
    global logger
    if not format_string:
        format_string = "%(asctime)s %(name)s %(levelname)s %(pathname)s:%(lineno)d " \
                        "%(process)d %(thread)d : %(message)s"  # see logging.__init__.Formatter()
    logger = logging.getLogger(name)
    logger.setLevel(level)
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(level)
    formatter = logging.Formatter(format_string, datefmt=None)  # the ISO8601 date format, 2018-12-11 15:01:17,290
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)


def debug_msg(msg, *args, **kwargs):
    # TODO(DingGuodong): a good debug function wanted
    # no qa
    if DEBUG:
        print("debug: {msg}".format(msg=msg))
        print("args: {args}".format(args=str(args)))
        print("kwargs: {kwargs}".format(kwargs=str(kwargs)))


def debug_msg_with_logging(msg, *args, **kwargs):
    """
    脚本调试函数，输出日志行到标准输出
    :param msg: str, 需要打印日志的普通字符串
    :param args: 需要打印日志的list、tuple等
    :param kwargs: 需要打印日志的字典
    :return:
    """
    if DEBUG:
        if not logger.handlers:  # block same/duplicate Log messages/entries multiple times
            set_stream_logger('dcobf', logging.INFO)  # debug cobf
        logger.debug(msg, *args, **kwargs)


def console_log_msg(msg, level="error", *args, **kwargs):
    """
    记录日志到指定的文件并按照日期切割
    :param msg: str, 需要打印日志的普通字符串
    :param level: str, 打印日志的级别，可以定义error、warn、debug、info等其他
    :param args: 需要打印日志的list、tuple等
    :param kwargs: 需要打印日志的字典
    :return:
    """
    if not logger.handlers:  # block same/duplicate Log messages/entries multiple times
        set_file_logger_date(self_script_output_log_path, name="cobf")
    if level.lower() == "error":
        logger.error(msg, *args, **kwargs)
    elif "warn" in level.lower():
        logger.warning(msg, *args, **kwargs)
    elif level.lower() == "debug":
        logger.debug(msg, *args, **kwargs)
    else:
        logger.info(msg, *args, **kwargs)


def get_keyword_from_name(name):
    """
    name type1: master2018-03-28 01.00.00.bak --> master
    name type2: master_backup_2020_05_15_145050_0886796.bak --> master
    name type3: ReportServer$MSSQL2K8R2TempDB_backup_2020_05_18_000003_2507890.bak --> ReportServer$MSSQL2K8R2TempDB
    :param name: database backup filename
    :type name: str
    :return: database name in filename
    :rtype: str
    """

    pattern = re.compile(r"^([A-Za-z_$]+)\d.*")
    match = pattern.match(name)
    if match:
        groups_tuple = match.groups()
        keyword = groups_tuple[0]
        if "_backup_" in keyword:
            return keyword.strip("_backup_")
        else:
            return keyword
    else:
        if DEBUG:
            debug_msg_with_logging(name)
        return None


def get_keyword_from_name_u1(name):
    """
    name type1: master2018-03-28 01.00.00.bak --> master
    name type2: master_backup_2020_05_15_145050_0886796.bak --> master
    name type3: ReportServer$MSSQL2K8R2TempDB_backup_2020_05_18_000003_2507890.bak --> ReportServer$MSSQL2K8R2TempDB
    :param name: database backup filename
    :type name: str
    :return: database name in filename
    :rtype: str
    """
    pattern = r'_backup_|\d{4}[-_]\d{2}[-_]\d{2}'
    split_list = re.split(pattern, name)
    # Note: len(split_list) >= 1
    return split_list[0]


def sort_files_by_ctime(files_list):
    return sorted(files_list, key=lambda x: os.path.getctime(x))


def get_sorted_dict(files_dict):
    # type: (dict)->dict
    for k, v in files_dict.iteritems():  # type: str, list
        files_dict[k].sort(key=lambda x: os.path.getctime(x), reverse=True)
    return files_dict


def get_all_files(path):
    files_list = []
    for top, dirs, nondirs in os.walk(path):
        files_list = [os.path.join(top, x) for x in nondirs]
        break

    files_dict = defaultdict(list)

    for backup_file in files_list:
        if backup_file.endswith(backup_file_extension):  # only processing file ext ends with ".bak"
            keyword = get_keyword_from_name_u1(os.path.basename(backup_file))
            files_dict[keyword].append(backup_file)

    if DEBUG:
        print(json.dumps(get_sorted_dict(files_dict), indent=4))

    return get_sorted_dict(files_dict)


if __name__ == '__main__':
    self_script_output_log_path = r"C:\clean-old-backup-files.log"
    backup_files_path_list = [r"D:\DataBackup\Daily", r"D:\SqlAutoBakup\Daily", r"E:\Data\SqlAutoBakup\Daily",
                              r"D:\MSSQL\Backup", r"D:\Data\SqlAutoBakup\Daily"]
    backup_file_extension = ".bak"
    save_days = 30

    if not any(os.path.exists(x) for x in backup_files_path_list):
        console_log_msg("No such file or directory", level="warn")
        sys.exit(0)

    for backup_files_path in backup_files_path_list:
        if os.path.exists(backup_files_path):
            console_log_msg("processing directory: {directory}".format(directory=backup_files_path), level="info")
            backups_dict = get_all_files(backup_files_path)
            for cur_keyword, cur_files_list in backups_dict.iteritems():
                console_log_msg("{keyword} has {count} backups.".format(keyword=cur_keyword, count=len(cur_files_list)),
                                level="info")
                for backup in cur_files_list[save_days:]:
                    # print("file \"{path}\" is deleted".format(path=backup))
                    console_log_msg("file \"{path}\" is deleted".format(path=backup), level="warn")
                    os.remove(backup)
    else:
        # print("no file is deleted, all files are ok.")
        console_log_msg("no file is deleted, all files are ok. ", level="warn")
        sys.exit(0)
