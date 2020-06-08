#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created by PyCharm.
File Name:              LinuxBashShellScriptForOps:remove-backup-files-to-keep-disk-usable.py
Version:                0.0.1
Author:                 dgden
Author Email:           dgdenterprise@gmail.com
URL:                    https://github.com/DingGuodong/LinuxBashShellScriptForOps
Download URL:           https://github.com/DingGuodong/LinuxBashShellScriptForOps/tarball/master
Create Date:            2020/6/8
Create Time:            11:40
Description:            remote backup files to keep disk usable (Avail disk space usage > 5GB )
Long Description:       已知有多台Windows服务器，每一台服务器上运行有SQL Server，每天服务器会在一些指定的目录下生成备份文件，
                        扩展名均为bak，备份已经经过SQL Server压缩，
                        需要使用脚本检查备份文件所在的磁盘空间大小，已经配置为定期清理备份，但由于磁盘空间不足，清理未必有效，
                        需要保证备份目录所在的磁盘可用空间>5GB，
                        如果空间低于5GB，则需要删除备份目录中较大的备份，直到空间大于5GB。
References:             
Prerequisites:          pip install psutil
Development Status:     3 - Alpha, 5 - Production/Stable
Environment:            Console
Intended Audience:      System Administrators, Developers, End Users/Desktop
License:                Freeware, Freely Distributable
Natural Language:       English, Chinese (Simplified)
Operating System:       Microsoft :: Windows
Programming Language:   Python :: 2.6
Programming Language:   Python :: 2.7
Topic:                  Utilities
 """
import os
import sys

import logging
import psutil
from logging.handlers import TimedRotatingFileHandler

logger = logging.getLogger('mylog')


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
        set_file_logger_date(self_script_output_log_path, name="rbftkdu")
    if level.lower() == "error":
        logger.error(msg, *args, **kwargs)
    elif "warn" in level.lower():
        logger.warning(msg, *args, **kwargs)
    elif level.lower() == "debug":
        logger.debug(msg, *args, **kwargs)
    else:
        logger.info(msg, *args, **kwargs)


def get_all_files(path):
    """
    get all backup files and put them into a list
    :param path: file path
    :type path: str
    :return:
    :rtype: list
    """
    files_list = []
    for top, dirs, nondirs in os.walk(path):
        files_list = [os.path.join(top, x) for x in nondirs if x.endswith(backup_file_extension)]
        break

    return files_list


def get_disk_usage_avail(disk):
    """
    get disk usage by disk label, such as 'C', 'D', "C:", "C:\\"
    :param disk: disk device label
    :type disk: str
    :return: disk usage
    :rtype:long
    """
    for partition in psutil.disk_partitions():
        # type:psutil._common.sdiskpart  # type: from collections import namedtuple
        if partition.device.startswith(disk):
            return psutil.disk_usage(partition.mountpoint).free


def remove_file(path):
    os.remove(path)  # nothing is returned


def is_can_remove_action(disk):
    """
    checkout if available disk usage < 5GB
    :param disk: disk label, such as 'C', 'D', "C:", "C:\\"
    :type disk: str
    :return: boolean
    :rtype: bool
    """
    min_avail_disk_size = 5 * 1024 * 1024 * 1024
    cur_disk_usage = get_disk_usage_avail(disk)
    if cur_disk_usage < min_avail_disk_size:
        return True
    else:
        return False


def sort_files_by_size(files_list):
    return sorted(files_list, key=lambda x: os.path.getsize(x), reverse=True)


def get_file_to_remove(files_list):
    """
    get the file's path with the largest file size
    :param files_list: the files' path
    :type files_list: list
    :return: file's path
    :rtype: str
    """
    sorted_files_list = sort_files_by_size(files_list)
    if len(sorted_files_list) > 0:
        return sorted_files_list[0]


if __name__ == '__main__':
    self_script_output_log_path = r"C:\remove-backup-files-to-keep-disk-usable.log"
    backup_files_path_list = [r"D:\DataBackup\Daily", r"D:\SqlAutoBakup\Daily", r"E:\Data\SqlAutoBakup\Daily",
                              r"D:\MSSQL\Backup", r"D:\Data\SqlAutoBakup\Daily"]
    backup_file_extension = ".bak"

    if not any(os.path.exists(x) for x in backup_files_path_list):
        console_log_msg("No such file or directory", level="warn")
        sys.exit(0)

    for backup_files_path in backup_files_path_list:
        if os.path.exists(backup_files_path):
            disk_label = backup_files_path[0]  # such as: "C", "D"
            keep_running_flag = True
            while keep_running_flag:
                if is_can_remove_action(disk_label):
                    now_disk_usage = get_disk_usage_avail(disk_label)
                    console_log_msg("disk '{}:' usage is not enough, {}".format(disk_label, now_disk_usage),
                                    level="warn")
                    backup_files_list = get_all_files(backup_files_path)
                    file_to_remove = get_file_to_remove(backup_files_list)
                    console_log_msg("file is deleted, {}".format(file_to_remove), level="warn")
                    remove_file(file_to_remove)
                else:
                    keep_running_flag = False
    else:
        console_log_msg("no file is deleted, all files are ok. ", level="warn")
        sys.exit(0)
