#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created by PyCharm.
File Name:              LinuxBashShellScriptForOps:backup-files-to-aliyun-oss.py
Version:                0.0.1
Author:                 Guodong
Author Email:           dgdenterprise@gmail.com
URL:                    https://github.com/DingGuodong/LinuxBashShellScriptForOps
Download URL:           https://github.com/DingGuodong/LinuxBashShellScriptForOps/tarball/master
Create Date:            2019/2/11
Create Time:            9:29
Description:            backup files to Aliyun OSS, GA Version
Long Description:
备份策略说明：          1. 为了提高备份效率以及节省OSS（备份存储后端）存储空间，考虑到部分文件（以站点附件为例）
                            只增不减，因此可以以当前年份（2019）为分割点，2019年前的实行按年压缩文件备份，
                            2019年的实行按照月压缩文件备份。
                        2. 为了使得备份文件有效，要执行日备份以及周备份，周备份保留1周以上，日备份保留2天以上
                        3. OSS上的定期删除使用OSS Bucket的生命周期规则功能
                        4. 其他可选方案：ossfs能把oss bucket挂载到本地，如果您使用的软件没有支持OSS，
                            但您又想让数据能自动同步到OSS，那么ossfs是很好的选择。
                            https://help.aliyun.com/document_detail/32197.html
                            但使用ossfs会导致失去隔离，攻击可能会扩散到OSS整个bucket，因此建议使用sdk并使用RAM子账号权限
备份路径设计参考：
                        1. 路径必须由ASCII字符表示，不能使用中文以及其他字符
                            /backup/<ecs-id>_<ip>_<site-id>/daily|weekly/<time:YY-mm-dd>/<file-type1>|<file-type2>/files
                        2. OSS 路径设计
                            在OSS中路径即前缀（prefix），因此建议设计如下：
                            <ip>_<site-id>_d|w_<time:YY-mm-dd>/files
References:
Prerequisites:          pip install --upgrade oss2
                        pip install -U netifaces
Development Status:     3 - Alpha, 5 - Production/Stable
Environment:            Console
Intended Audience:      System Administrators, Developers, End Users/Desktop
License:                Freeware, Freely Distributable
Natural Language:       English, Chinese (Simplified)
Operating System:       POSIX :: Linux, Microsoft :: Windows
Programming Language:   Python :: 3

Topic:                  Utilities
 """
import json
import logging
import netifaces
import os
import platform
import random
import re
import string
import tarfile
import time
from collections import Iterable
from logging.handlers import RotatingFileHandler, TimedRotatingFileHandler

import oss2
from oss2.models import LifecycleExpiration, LifecycleRule, BucketLifecycle

# 初始化logger，用于记录日志
logger = logging.getLogger('mylog')


def set_file_logger(filename, name="mylog", level=logging.INFO, format_string=None):
    global logger
    if not format_string:
        format_string = "%(asctime)s %(name)s %(levelname)s %(pathname)s:%(lineno)d %(module)s %(funcName)s " \
                        "%(process)d %(thread)d : %(message)s"  # see logging.__init__.Formatter()
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
        format_string = "%(asctime)s %(name)s %(levelname)s %(pathname)s:%(lineno)d %(module)s %(funcName)s " \
                        "%(process)d %(thread)d : %(message)s"  # see logging.__init__.Formatter()
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
        format_string = "%(asctime)s %(name)s %(levelname)s %(pathname)s:%(lineno)d %(module)s %(funcName)s " \
                        "%(process)d %(thread)d : %(message)s"  # see logging.__init__.Formatter()
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
        format_string = "%(asctime)s %(name)s %(levelname)s %(pathname)s:%(lineno)d %(module)s %(funcName)s " \
                        "%(process)d %(thread)d : %(message)s"  # see logging.__init__.Formatter()
    logger = logging.getLogger(name)
    logger.setLevel(level)
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(level)
    formatter = logging.Formatter(format_string, datefmt=None)  # the ISO8601 date format, 2018-12-11 15:01:17,290
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)


# 启用文件日志，按照日期切割
set_file_logger_date("backup.log")

# 以下字典（本服务配置）暂未使用
SERVICE_CONFIG = {
    "public_ip_addr": "",
    "backup_path": [
        {
            "site_name": "",
            "site_url": "",
            "site_path": "",
        },
        {
            "site_name": "",
            "site_url": "",
            "site_path": "",
        },
    ]
}

# 加载阿里云AccessKey和OSS bucket配置信息
with open('config.json') as fp:
    info = fp.read()
    ak = json.loads(info)["access_key"][0]
    bucket_info = json.loads(info)["bucket_info"][0]

access_key_id = os.getenv('OSS_TEST_ACCESS_KEY_ID', ak.get('AccessKeyID'))
access_key_secret = os.getenv('OSS_TEST_ACCESS_KEY_SECRET', ak.get('AccessKeySecret'))
bucket_name = os.getenv('OSS_TEST_BUCKET', bucket_info.get('name'))
endpoint = os.getenv('OSS_TEST_ENDPOINT', bucket_info.get('endpoint'))


def to_unicode_or_bust(obj, encoding='utf-8'):
    # the function convert non-unicode object to unicode object
    if isinstance(obj, str):
        if not isinstance(obj, str):
            obj = str(obj, encoding)

    return obj


def to_str_or_bust(obj, encoding='utf-8'):
    # the function convert unicode object to str object
    if isinstance(obj, str):
        if isinstance(obj, str):
            obj = obj.encode(encoding)

    return obj


def fn_timer_py2py3(func):
    """
    测量函数执行所用时间的装饰器（调试和性能评估时使用）
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
            print(e)
        time_end = time.time()
        message = "Total time running {func_name}: {time_spent:16.8f} seconds".format(func_name=func.__name__,
                                                                                      time_spent=time_end - time_begin)
        logger.info(message)
        return result

    return func_timer


def get_node_info():
    """
    return default ipv4 and hostname of the computer where the Python interpreter is running

    Microsoft Visual C++ Compiler for Python 2.7 maybe need installed or reinstalled.
    See also: https://www.microsoft.com/en-us/download/confirmation.aspx?id=44266
    It can be download here: \
    https://download.microsoft.com/download/7/9/6/796EF2E4-801B-4FC4-AB28-B59FBF6D907B/VCForPython27.msi

    :return:
    """
    default_ipv4 = '127.0.0.1'

    for interface in netifaces.interfaces():
        if interface == netifaces.gateways()['default'][netifaces.AF_INET][1]:
            try:
                default_ipv4 = netifaces.ifaddresses(interface)[netifaces.AF_INET][0]['addr']
            except KeyError:
                pass

    return default_ipv4, platform.node()


def prepare():
    """
    make sure enough disk space available
    make sure network is enabled
    :return:
    """
    logger.info("preparing for backup.")
    # TODO(Guodong) not now


@fn_timer_py2py3
def upload_oss(path, name):
    """
    :param path:
    :param name: name is filename stored on OSS, which known as 'key' in oss2.
    :return:
    """
    # KNOWN ISSUE: oss2 has a bug in oss2.resumable_upload() which not support non-ascii character

    path = to_unicode_or_bust(path)  # support support non-ascii character, such as path name in Chinese Language

    bucket = oss2.Bucket(oss2.Auth(access_key_id, access_key_secret), endpoint, bucket_name)

    if not os.path.exists(path):  # need <type 'unicode'>
        raise OSError("cannot access '%s': No such file or directory" % to_str_or_bust(path))
    else:
        logger.info("file \'%s\' selected." % path)

    if name:
        # OSS中的目录/文件夹概念
        # https://help.aliyun.com/knowledge_detail/39527.html
        key = name
    else:
        key = os.path.basename(path)

    path = to_str_or_bust(path)
    key = to_str_or_bust(key)

    logger.info("ready for uploading file to oss")
    result = oss2.resumable_upload(bucket, key, path, multipart_threshold=10 * 1024 * 1024)

    oss_obj = bucket.get_object(key)
    logger.info(" ".join((oss_obj.request_id, str(oss_obj.status))))
    logger.info("file \'%s\' uploaded." % path)
    return result


@fn_timer_py2py3
def set_oss_file_expired(prefix, days=3):
    """
    关于prefix:
    https://help.aliyun.com/knowledge_detail/39527.html
    OSS中的文件夹其实是一个大小为0KB的空文件。因此，用户创建一个key值为1/的object就会定义文件夹1；
    并且如果用户创建文件abc/1.jpg，系统是不会创建abc/这个文件的，因此在删除abc/1.jpg后将不会再存在abc这个文件夹。

    在后端存储的过程中不同的文件夹的文件仅仅是key值的前缀不一样。
    所有文件的key值（这里需要通过prefix指定文件夹）
    :param prefix: prefix for key,
    :param days: save days
    :return:
    """
    logger.info("setting expired time started")
    bucket = oss2.Bucket(oss2.Auth(access_key_id, access_key_secret), endpoint, bucket_name)

    rule1 = LifecycleRule('rule1', prefix,
                          status=LifecycleRule.ENABLED,
                          expiration=LifecycleExpiration(days=days))

    lifecycle = BucketLifecycle([rule1])

    result = bucket.put_bucket_lifecycle(lifecycle)

    logger.info(" ".join((result.request_id, str(result.status))))
    logger.info("setting expired time finished")

    return result


@fn_timer_py2py3
def compress_files(name, path):
    """
    compress files or directory using tar in python
    :param name: tgz filename, the name can be a full path of name
    :param path: path to file or directory
    :return:
    """
    with tarfile.open(name, "w:gz") as tar:
        tar.add(path, arcname=os.path.basename(path))


@fn_timer_py2py3
def is_large_file(path):
    """
    check if file is a large file which size more than 700MB
    :param path:
    :return:
    """
    DEFINED_LARGE_FILE_SIZE = 700 * 1024 * 1024  # 700MB,A standard 120 mm, 700 MB CD-ROM

    path = to_unicode_or_bust(path)  # support support non-ascii character, such as path name in Chinese Language

    if os.path.isfile(path):
        if os.path.getsize(path) > DEFINED_LARGE_FILE_SIZE:
            return True
        else:
            return False
    else:
        raise OSError("cannot access '%s': No such file or directory" % to_str_or_bust(path))


def split_large_file_by_line(path, line=40000):
    """
    https://stackoverflow.com/questions/8096614/split-large-files-using-python
    :param: path: path to split
    :return:
    """
    NUM_OF_LINES = line or 40000

    path = to_unicode_or_bust(path)  # support support non-ascii character, such as path name in Chinese Language

    if os.path.isfile(path):
        with open(path, "rb") as fin:
            fout = open(path + "_part0", "wb")
            for i, line in enumerate(fin):
                fout.write(line)
                if (i + 1) % NUM_OF_LINES == 0:
                    fout.close()
                    fout = open(path + "_part%d" % (i / NUM_OF_LINES + 1), "wb")

            fout.close()
        pass


def split_large_file_by_size(path, size=734003200):
    """
    :param: path: path to split
    :return:
    """
    CHUNK_SIZE = size or 734003200

    path = to_unicode_or_bust(path)  # support support non-ascii character, such as path name in Chinese Language

    part_num = 0
    if os.path.isfile(path):
        with open(path, "rb") as fin:
            while True:
                chunk = fin.read(CHUNK_SIZE)
                if not chunk:
                    break
                with open(path + "_part%d" % part_num, 'wb') as fout:
                    fout.write(chunk)
                part_num += 1
        pass


def get_latest_files(path):
    """
    return the files which created today
    :param path:
    :return:
    """
    path = to_unicode_or_bust(path)  # support support non-ascii character, such as path name in Chinese Language

    files = os.listdir(path)
    files_chosen = list()

    today = time.strftime('%Y-%m-%d', time.localtime(time.time()))

    for item in files:
        full_path = os.path.abspath(os.path.join(path, item))
        created_time = time.strftime('%Y-%m-%d', time.localtime(os.path.getmtime(full_path)))
        if created_time == today:
            files_chosen.append(full_path)
    return files_chosen


def __getmtime(path):
    path = to_unicode_or_bust(path)  # support support non-ascii character, such as path name in Chinese Language
    if os.path.exists(path):
        return os.path.getmtime(path)
    else:
        # KNOWN ISSUE: os.path.exists may return False when "®"(copyright sign) in filename
        # PEP 277 -- Unicode file name support for Windows NT
        # https://www.python.org/dev/peps/pep-0277/
        return 0


def sort_files_by_mtime(path):
    """
    path can be basestring type or iterable
    :param path:
    :return:
    """
    if isinstance(path, str):
        if os.path.isdir(path):
            os.chdir(path)  # essential for os.path.abspath
            files = os.listdir(path)
    elif isinstance(path, Iterable):
        files = path
    else:
        return []

    for index, item in enumerate(files):
        files[index] = to_unicode_or_bust(os.path.abspath(item).decode("gbk"))

    return sorted(files, key=__getmtime, reverse=True)


def get_core_name_from_file(name):
    """
    get core name from filename
    :param name:
    :return:
    """
    pattern = re.compile(".*OSAP_(.*?)[0-9].*bak")
    match = pattern.match(name)
    if match:
        return match.groups()[0]
    else:
        return ''.join(random.choice(string.ascii_lowercase) for _ in range(10))


def shrink_database():
    """
    shrink LDF file in MS SQL SERVER
    :return:
    """
    # TODO(Guodong) not now
    pass


@fn_timer_py2py3
def backup_attachments():
    """
    D:\WWW\TianYuan\osap\Temp
    D:\WWW\TianYuan\osap\policyfiles
    D:\WWW\TianYuan\osap\Doc\Customer|Employee|GOV|System

    TODO(Guodong) 由于附件系统设计过于复杂，暂时不设计为使用脚本备份，而使用磁盘快照备份方式
    :return:
    """
    pass


@fn_timer_py2py3
def backup_databases(days=2):
    """
    备份数据库的核心函数，完成的操作（含函数调用）有：
        1. 筛选数据库文件，选择哪些文件需要备份
        2. 压缩文件，如果大于10GB则意味着文件需要额外处理
        3. 上传文件到OSS
        4. 配置OSS object 过期时间（生命周期）
        5. 删除临时文件
    :return:
    """
    to_backup_dir = r"D:\Data\SqlAutoBakup\Daily"
    save_days = days

    if save_days >= 7:
        bak_type = "weekly"
    else:
        bak_type = "daily"

    node_ip, node_name = get_node_info()
    today = time.strftime('%Y%m%d', time.localtime(time.time()))

    files_to_process = get_latest_files(to_backup_dir)
    files_to_process = sort_files_by_mtime(files_to_process)

    for item in files_to_process:
        logger.info("%s has been started" % item)

        item_size = os.path.getsize(item)

        if item_size > 10 * 1024 * 1024 * 1024:
            # TODO(Guodong) not now: split large file to small files
            shrink_database()
            logger.error("this file need be shrunken." % item)
        else:
            basename = os.path.basename(item)
            core_name = get_core_name_from_file(basename)
            tarfile_name = "_".join((node_ip, today, core_name)) + ".tgz"

            logger.info("compressing file \'%s\'" % item)
            compress_files(tarfile_name, item)

            tarfile_size = os.path.getsize(tarfile_name)
            logger.info(
                " ".join((str(tarfile_size), str(item_size), "%.6f%%" % (float(tarfile_size) / item_size * 100))))
            logger.info("file \'%s\' compressed." % item)

            oss_prefix = "%s_db_%s/" % (node_ip, bak_type)
            upload_oss(os.path.abspath(tarfile_name), oss_prefix + tarfile_name)
            set_oss_file_expired(oss_prefix, days=save_days)

            # Next, delete tmp files
            if os.path.exists(tarfile_name):
                os.remove(tarfile_name)

            logger.info("%s has been finished" % item)


def validate():
    """
    check files backuped on OSS
    :return:
    """
    # TODO(Guodong) not now
    pass


@fn_timer_py2py3
def main():
    logger.info("backup operation is in processing")
    backup_databases(days=7)
    logger.info("backup operation has been finished")


if __name__ == '__main__':
    main()
