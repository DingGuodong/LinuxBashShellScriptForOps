#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created by PyCharm.
File Name:              LinuxBashShellScriptForOps:clean-old-backup-files-v2.py
Version:                0.0.1
Author:                 dgden
Author Email:           dgdenterprise@gmail.com
URL:                    https://github.com/DingGuodong/LinuxBashShellScriptForOps
Download URL:           https://github.com/DingGuodong/LinuxBashShellScriptForOps/tarball/master
Create Date:            2020/3/3
Create Time:            17:17
Description:            clean old backup files, save backups for x days, y weeks and z months
in this case, it will save 5 + 1 (1 also in 4 weekly bak) monthly bak, 4 weekly bak, 7 daily bak, 16 total
Long Description:       本脚本用于每日备份后的删除清理操作，可以在备份操作后进行，
                        通过每日备份配合删除操作，可生成一定数量的月备份、周备份和日备份，满足本地备份保留多个时间段的需求
                        本地备份策略：
                            每日备份1次，定期删除旧备份备份
                                建议1：每日备份保留9个，每周备份保留5个，每月备份保留7个
                                建议2：每日备份保留7个，每周备份保留4个，每月备份保留6个
                        异地备份策略：
                            使用快照进行，或在有条件的情况下将数据传输到OSS对象存储服务
                                建议：每日快照保存3天，周快照保存8天
References:             注释风格：reStructuredText docstring format
                        [pyCharm中添加方法注释]https://blog.csdn.net/dkjkls/article/details/88933950

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

import datetime
import logging
import time
from logging.handlers import RotatingFileHandler, TimedRotatingFileHandler

# from dateutil.relativedelta import relativedelta  # pip install -U python-dateutil

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
    return sorted(files_list, key=lambda x: os.path.getctime(x), reverse=True)


def get_sorted_dict(files_dict):
    # type: (dict)->dict
    for k, v in files_dict.iteritems():  # type: str, list # and len(list[0]) = 1
        files_dict[k].sort(key=lambda x: os.path.getctime(x), reverse=True)
    return files_dict


def get_sorted_dict_l2(files_dict):
    # type: (dict)->dict
    for k, v in files_dict.iteritems():  # type: str, list # and len(list[0]) = 2
        files_dict[k].sort(key=lambda x: os.path.getctime(x[0]), reverse=False)
    return files_dict


def get_date_of_file(path):
    """
    :param path: str
    :return: str
    """
    return datetime.datetime.fromtimestamp(os.path.getctime(path)).strftime("%Y%m%d")


def get_all_files(path):
    """
    get all backup files and put them into a dict
    :param path:
    :return:
    """
    files_list = []
    for top, dirs, nondirs in os.walk(path):
        files_list = [os.path.join(top, x) for x in nondirs]
        break

    files_dict = defaultdict(list)

    for backup_file in files_list:
        if backup_file.endswith(backup_file_extension):  # only processing file ext ends with ".bak"
            keyword = get_keyword_from_name_u1(os.path.basename(backup_file))
            # TODO(DingGuodong) add get_date_of_file() is not essential, but it(files_dict) can be extend easily
            files_dict[keyword].append((backup_file, get_date_of_file(backup_file)))

    if DEBUG:
        print(json.dumps(get_sorted_dict_l2(files_dict), indent=4))

    return get_sorted_dict_l2(files_dict)


def is_ctime_same_month(left, right):
    left_ctime_month = datetime.datetime.fromtimestamp(os.stat(left).st_ctime).month
    right_ctime_month = datetime.datetime.fromtimestamp(os.stat(right).st_ctime).month
    return left_ctime_month == right_ctime_month


def is_ctime_same_week(left, right):
    left_ctime_week_number = datetime.datetime.fromtimestamp(os.stat(left).st_ctime).isocalendar()[1]
    right_ctime_week_number = datetime.datetime.fromtimestamp(os.stat(right).st_ctime).isocalendar()[1]
    return left_ctime_week_number == right_ctime_week_number


def delete_invalid_backup_files(files_list):
    """
    save 5 + 1 (1 also in 4 weekly bak) monthly bak, 4 weekly bak, 7 daily bak
    after delete invalid backup files, there will are 5 monthly bak, 4 weekly bak, 7 daily bak
    :param files_list: sorted by ctime, [older, newer,]
    :type files_list: list
    :return:
    :rtype:
    """
    valid_monthly_list = list()
    valid_weekly_list = list()
    valid_daily_list = list()

    for item in files_list:  # ('D:\\XXXX\\Daily\\XXXX_backup_2020_07_13_000001_2502839.bak', '20200713')
        path = item[0]
        file_stat_result = os.stat(path)
        timedelta = time.time() - file_stat_result.st_ctime

        if timedelta > 6 * 30 * 24 * 3600:  # delete backups older than 6 months
            reason = "old than 6 months"
            console_log_msg("file \"{path}\" is deleted, reason: {reason}".format(path=path, reason=reason),
                            level="warn")
            os.remove(path)
        elif timedelta > 1 * 30 * 24 * 3600:  # bak is between 1 mon and 6 mon
            if len(valid_monthly_list) > 0:
                if is_ctime_same_month(valid_monthly_list[-1], path):
                    reason = "can be safe removed by months"
                    console_log_msg("file \"{path}\" is deleted, reason: {reason}".format(path=path, reason=reason),
                                    level="warn")
                    os.remove(path)
                else:
                    valid_monthly_list.append(path)
            else:
                valid_monthly_list.append(path)
        elif timedelta > 1 * 7 * 24 * 3600:  # bak is between 1 week and 4 week
            if len(valid_weekly_list) > 0:
                if is_ctime_same_week(valid_weekly_list[-1], path):
                    reason = "can be safe removed by weekly"
                    console_log_msg("file \"{path}\" is deleted, reason: {reason}".format(path=path, reason=reason),
                                    level="warn")
                    os.remove(path)
                else:
                    valid_weekly_list.append(path)
            else:
                valid_weekly_list.append(path)
        else:  # bak is newer than 1 week
            valid_daily_list.append(path)

    # remove extra backups which not needed
    if len(valid_monthly_list) > 6:  # save only 6 months
        invalid_monthly_list = valid_monthly_list[6:]
        for path in invalid_monthly_list:
            reason = "can be safe removed by monthly upto 6"
            console_log_msg("file \"{path}\" is deleted, reason: {reason}".format(path=path, reason=reason),
                            level="warn")
            os.remove(path)
    if len(valid_weekly_list) > 4:  # save only 4 weeks
        invalid_weekly_list = valid_weekly_list[4:]
        for path in invalid_weekly_list:
            reason = "can be safe removed by weekly upto 4"
            console_log_msg("file \"{path}\" is deleted, reason: {reason}".format(path=path, reason=reason),
                            level="warn")
            os.remove(path)

    return valid_daily_list + valid_weekly_list[:4] + valid_monthly_list[:6]


if __name__ == '__main__':
    self_script_output_log_path = r"C:\clean-old-backup-files-v3.log"
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
                result = delete_invalid_backup_files(cur_files_list)
                console_log_msg("valid backups are: {}".format(", ".join(result)), level='debug')
    else:
        # print("no file is deleted, all files are ok.")
        console_log_msg("no file is deleted, all files are ok. ", level="warn")
        sys.exit(0)
