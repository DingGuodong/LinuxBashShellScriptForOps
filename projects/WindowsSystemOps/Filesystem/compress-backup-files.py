#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created by PyCharm.
File Name:              LinuxBashShellScriptForOps:compress-backup-files.py
Version:                0.0.1
Author:                 dgden
Author Email:           dgdenterprise@gmail.com
URL:                    https://github.com/DingGuodong/LinuxBashShellScriptForOps
Download URL:           https://github.com/DingGuodong/LinuxBashShellScriptForOps/tarball/master
Create Date:            2020/2/21
Create Time:            19:17
Description:            compress backup file to rar or gz using multiprocessing to save disk space
Long Description:
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
import subprocess
import sys
import tarfile
from multiprocessing import Pool

import logging
from logging.handlers import RotatingFileHandler, TimedRotatingFileHandler

DEBUG = False

self_script_output_log_path = r"compress-backup-files.log"
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


def run_command(executable):
    """
    run system command by subprocess.Popen in silent
    :param executable: executable command
    :return: return_code, stdout, stderr
    """
    proc_obj = subprocess.Popen(executable, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = proc_obj.communicate()
    return_code = proc_obj.returncode
    return return_code, stdout, stderr


def compress_file_by_tar(path):
    console_log_msg("tar is compressing file \"{path}\"".format(path=path), level="warn")

    os.chdir(os.path.dirname(path))
    name = os.path.basename(path) + ".tgz"
    with tarfile.open(name, "w:gz") as tar:
        tar.add(path, arcname=os.path.basename(path))


def compress_file_by_rar(path):
    console_log_msg("rar is compressing file \"{path}\"".format(path=path), level="warn")

    os.chdir(os.path.dirname(path))
    if not os.path.exists(RAR_EXE_PATH):
        return False

    command = " ".join(
        ("\"{rar}\"".format(rar=RAR_EXE_PATH), RAR_EXE_ARGUMENT.format(name=os.path.basename(path), path=path)))
    console_log_msg(command)

    return_code, stdout, stderr = run_command(command)
    if return_code == 0:
        return True
    else:
        console_log_msg(
            "compressing file \"{path}\" by rar failed, "
            "with reason {stdout}, {stderr}".format(path=path, stdout=stdout, stderr=stderr),
            level="warn")
        return False


def compress_then_delete(path):
    is_compress_ok = compress_file_by_rar(path)
    if not is_compress_ok:
        compress_file_by_tar(path)

    console_log_msg("file \"{path}\" is deleted".format(path=path), level="warn")
    os.remove(path)


def do_task_with_multiprocessing(files_list):
    pool = Pool(2)  # 2 CPU cores
    # [Keyboard Interrupts with python's multiprocessing Pool](
    # https://stackoverflow.com/questions/1408356/keyboard-interrupts-with-pythons-multiprocessing-pool)
    # [Python 中 Ctrl+C 不能终止 Multiprocessing Pool 的解决方案](https://segmentfault.com/a/1190000004172444)
    pool.map_async(compress_then_delete, files_list).get(timeout=99999)  # 99999 > 86400(60 * 60 * 24)


RAR_EXE_PATH = r"C:\Program Files\WinRAR\Rar.exe"
RAR_EXE_ARGUMENT = "a -ep \"{name}.rar\" \"{path}\""  # pay attention to "space(' ')" in Microsoft Windows Path

if __name__ == '__main__':
    backup_files_path_list = [r"D:\DataBackup\Daily", r"D:\SqlAutoBakup\Daily"]
    backup_file_extension = ".bak"

    if not any(os.path.exists(x) for x in backup_files_path_list):
        sys.exit(0)

    for backup_files_path in backup_files_path_list:
        if os.path.exists(backup_files_path):
            console_log_msg("processing directory: {directory}".format(directory=backup_files_path), level="info")
            backup_files_list = []
            for top, dirs, nondirs in os.walk(backup_files_path):
                backup_files_list = [os.path.join(top, x) for x in nondirs if x.endswith(backup_file_extension)]
                break
            do_task_with_multiprocessing(backup_files_list)
