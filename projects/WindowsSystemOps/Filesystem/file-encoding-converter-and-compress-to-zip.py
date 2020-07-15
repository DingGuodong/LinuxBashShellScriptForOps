#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created by PyCharm.
File Name:              LinuxBashShellScriptForOps:file-encoding-converter-and-compress-to-zip.py
Version:                0.0.1
Author:                 dgden
Author Email:           dgdenterprise@gmail.com
URL:                    https://github.com/DingGuodong/LinuxBashShellScriptForOps
Download URL:           https://github.com/DingGuodong/LinuxBashShellScriptForOps/tarball/master
Create Date:            2020/6/10
Create Time:            15:09
Description:            convert file encoding utf-16 to utf-8 then zip it
Long Description:       file encoding converter, compress files using zip
References:             [UTF-8, UTF-16, UTF-32 & BOM](https://unicode.org/faq/utf_bom.html)
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

FAQ:
    Q: UnicodeDecodeError: 'utf16' codec can't decode byte 0x0a in position 245098: truncated data
    A: use try..except to catch exception, then verify it
    [python 读取utf-16时缺少字节的处理](https://blog.csdn.net/roymno2/article/details/71628128)
    Tips: it can use 'notepad++'(npp) with the shortcut key 'Ctrl+G' to goto the offset or position of file

 """
import os
import zipfile

import chardet
import datetime
import logging
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


def console_log_msg(msg, level="error", name="mylog", *args, **kwargs):
    """
    记录日志到指定的文件并按照日期切割
    :param msg: str, 需要打印日志的普通字符串
    :param level: str, 打印日志的级别，可以定义error、warn、debug、info等其他
    :param name: str, set the logger with the specified name
    :param args: 需要打印日志的list、tuple等
    :param kwargs: 需要打印日志的字典
    :return:
    """
    if not logger.handlers:  # block same/duplicate Log messages/entries multiple times
        set_file_logger_date(self_script_output_log_path, name=name, level=logging.DEBUG)
    if level.lower() == "error":
        logger.error(msg, *args, **kwargs)
    elif "warn" in level.lower():
        logger.warning(msg, *args, **kwargs)
    elif level.lower() == "debug":
        logger.debug(msg, *args, **kwargs)
    else:
        logger.info(msg, *args, **kwargs)


def timeit(func):
    """
    测量函数执行所用时间的装饰器
    https://stackoverflow.com/questions/8885663/how-to-format-a-floating-number-to-fixed-width-in-python
    :param func:
    :return:
    """
    from functools import wraps

    @wraps(func)
    def func_timer(*args, **kwargs):
        import time
        time_begin = time.time()
        result = None
        try:
            result = func(*args, **kwargs)
        except Exception as e:
            print(e.message)
        time_end = time.time()
        msg = "Total time running {func_name}: {time_spent:16.8f} seconds".format(func_name=func.__name__,
                                                                                  time_spent=time_end - time_begin)
        console_log_msg(msg, level='debug')
        return result

    return func_timer


@timeit
def is_file_encoding_with_utf8_or_utf16(path, encoding='utf-8'):
    """
    usage:
        is_file_encoding_with_utf8_or_utf16("test_utf8.csv", 'utf-8') -> True
        is_file_encoding_with_utf8_or_utf16("test_utf8.csv", 'utf-16') -> False
        is_file_encoding_with_utf8_or_utf16("test_utf16.csv", 'utf-16') -> True
        is_file_encoding_with_utf8_or_utf16("test_utf16.csv", 'utf-8') -> False
    :param path: file's path
    :type path: str
    :param encoding: 'utf-8' or 'utf-16'
    :type encoding: str
    :return: boolean
    :rtype:  bool
    """
    encoding = encoding.lower()
    if encoding not in ['utf-8', 'utf-16']:
        raise ValueError("bad encoding, only 'utf-8' or 'utf-16' is allowed.")

    if os.path.exists(path):
        with open(path, 'r') as fp:
            content = fp.read()
            if len(content) > 2048:  # improve performance when processing large file
                content = content[:2048]

        try:
            _ = content.decode(encoding)
        except UnicodeDecodeError:
            rlc = False  # low credibility
        else:
            rlc = True

        encoding_from_chardet_raw = chardet.detect(content).get("encoding")
        if encoding_from_chardet_raw:
            encoding_from_chardet = encoding_from_chardet_raw.lower()
            try:
                _ = content.decode(encoding_from_chardet)
            except UnicodeDecodeError:
                rmc = False  # medium credibility
            else:
                rmc = True
        else:
            rmc = False
            encoding_from_chardet = ""

        if rmc and (encoding in encoding_from_chardet):
            return True  # high credibility
        elif rmc and (encoding not in encoding_from_chardet):
            return False  # high credibility
        elif not rmc and (encoding in encoding_from_chardet):
            return False  # high credibility
        elif rlc:
            return True
        else:
            return False

    else:
        return False


@timeit
def convert_file_from_utf16_to_utf8(path):
    """
    :param path: file path
    :type path: str
    :return: success code
    :rtype: bool
    """
    if not is_file_encoding_with_utf8_or_utf16(path, 'utf-8'):
        msg = "{msg}: {path}".format(msg="file change encoding in progress: ", path=path)
        console_log_msg(msg, level="debug")

        with open(path, 'rb') as fp1:  # in py2, codecs.open(path, 'r','utf-16') -> unicode
            content = fp1.read()

        try:
            wanted_content = content.decode("utf-16").encode("utf-8")
        except UnicodeDecodeError as e:
            msg = "caught e: {msg}: {path} : try ignore".format(msg=str(e), path=path)
            console_log_msg(msg, level='warn')

            try:
                wanted_content = content.decode("utf-16", "ignore").encode("utf-8")
            except UnicodeDecodeError as e:
                msg = "{msg}: {path}".format(msg=str(e), path=path)
                console_log_msg(msg, level='error')
                return False

        with open(path, 'wb') as fp2:
            # # source: Little-endian UTF-16 Unicode text, with CRLF, CR line terminators
            # # output: UTF-8 Unicode (with BOM) text, with CRLF line terminators
            # fp2.write(content.decode("utf-16le").encode("utf-8"))

            # source: Little-endian UTF-16 Unicode text, with CRLF, CR line terminators
            # output: UTF-8 Unicode text, with CRLF line terminators
            fp2.write(wanted_content)
        return True

    else:
        msg = "{msg}: {path}".format(msg="file encoding is ok", path=path)
        console_log_msg(msg, level="info")


@timeit
def zip_compress(name, files, arc, keep_name=True):
    """
    compress files using zip
    :param name: zip file name, such as 'x.zip'
    :type name: str
    :param files: files to compress
    :type files: str or list
    :param arc: a absolute path, the top path of files
    :type arc: str
    :param keep_name: whether keep the parent directory name of files
    :type keep_name: bool
    :return: None
    :rtype: None
    """
    if isinstance(files, str):
        files_list = [files]
    elif isinstance(files, list):
        files_list = files
    else:
        raise RuntimeError

    with zipfile.ZipFile(name, 'w', compression=zipfile.ZIP_DEFLATED) as fp:
        for origin_file in files_list:
            if keep_name:
                parent = os.path.basename(arc)
                cur_arc = origin_file.replace(arc, "").strip(os.sep)
                archive_name = os.sep.join((parent, cur_arc))
            else:
                archive_name = origin_file.replace(arc, "")
            fp.write(origin_file, arcname=archive_name)


@timeit
def compress_src_directory_to_dst(save_name, source):
    if os.path.isdir(source):
        # put all files wanted into a list obj
        wanted_files_list = list()
        for top, dirs, nondirs in os.walk(source_path):
            # WARNING: some empty folder which has no file will not add zip
            for filename in nondirs:
                cur_file = os.path.join(top, filename)
                is_success = convert_file_from_utf16_to_utf8(cur_file)
                if is_success:
                    wanted_files_list.append(cur_file)

        if wanted_files_list:
            zip_compress(save_name, wanted_files_list, arc=source, keep_name=False)


if __name__ == '__main__':
    start_time = datetime.datetime.now()
    console_log_msg("-------- BEGIN: this task is in processing. --------", level='info')

    self_script_output_log_path = r"C:\file-encoding-converter-and-compress-to-zip.log"

    # source data path
    source_path = r"D:\WWW\DingLvAnHou\Databakup"

    # generate save as name
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    base_name = os.path.basename(source_path)
    save_as_filename = base_name + today + ".zip"
    save_as_path = r"D:\WWW\DingLvAnHou\DataBak"
    save_as_zip = os.path.join(save_as_path, save_as_filename)

    # compress source data
    compress_src_directory_to_dst(save_as_zip, source_path)

    used_seconds_str = str((datetime.datetime.now() - start_time).total_seconds())
    console_log_msg("-------- END: all task finished in {} seconds. --------".format(used_seconds_str), level='info')
