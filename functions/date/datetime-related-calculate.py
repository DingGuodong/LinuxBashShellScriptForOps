#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created by PyCharm.
File Name:              LinuxBashShellScriptForOps:datetime-related-calculate.py
Version:                0.0.1
Author:                 dgden
Author Email:           dgdenterprise@gmail.com
URL:                    https://github.com/DingGuodong/LinuxBashShellScriptForOps
Download URL:           https://github.com/DingGuodong/LinuxBashShellScriptForOps/tarball/master
Create Date:            2020/3/25
Create Time:            17:30
Description:            some useful functions about datetime related
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

import datetime
import random
import time
from itertools import repeat

import pytz


def generate_time():
    """
    生成一个格式为“%H%M”时间字符串
    :return: str
    """
    hour = random.choice(range(0, 24))
    minute = random.choice(range(0, 60))
    wanted_time = "{hour}:{minute:02d}".format(hour=str(hour).zfill(2), minute=minute)  # 填充，格式化，str format
    return wanted_time


def generate_time_list(num):
    """
    生成多个“重复”对象
    :param num:
    :return:
    """
    return [x() for x in repeat(generate_time, num)]


def compare_two_time(left, right, date_format="%H:%M"):
    """
    排序参数函数，比较两个时间的大小

    sorted(res_raw, cmp=lambda x, y: compare_two_time(x, y))
    :param left:
    :param right:
    :param date_format:
    :return: int
    """
    date_minuend = datetime.datetime.strptime(left, date_format)
    date_subtrahend = datetime.datetime.strptime(right, date_format)
    if date_minuend > date_subtrahend:
        return 1
    else:
        return -1


def get_seconds_from_two_time(left, right, date_format="%H:%M"):
    date_minuend = datetime.datetime.strptime(left, date_format)
    date_subtrahend = datetime.datetime.strptime(right, date_format)
    return (date_minuend - date_subtrahend).seconds


def get_minutes_from_time(time_str, date_format="%H:%M"):
    """
    计算时间包含的分钟数
    :param time_str:
    :param date_format:
    :return:
    """
    date = datetime.datetime.strptime(time_str, date_format)
    return date.hour * 60 + date.minute


def get_minutes_from_two_time(left, right, date_format="%H:%M"):
    return abs(get_minutes_from_time(left, date_format) - get_minutes_from_time(right, date_format))


def get_days_between_two_date(a, b, date_format="%Y%m%d"):
    date_minuend = datetime.datetime.strptime(a, date_format)
    date_subtrahend = datetime.datetime.strptime(b, date_format)
    return (date_minuend - date_subtrahend).days


def localtime_to_utc_iso8601(date, l_date_format="%Y%m%d%H%M%S", l_timezone='Asia/Shanghai',
                             r_date_format="%Y-%m-%dT%H:%M:%S.%fZ"):
    utc_date = datetime.datetime.strptime(date, l_date_format).replace(tzinfo=pytz.timezone(l_timezone)).astimezone(
        pytz.timezone('UTC'))
    utc_iso8601_date = utc_date.strftime(r_date_format)
    return utc_iso8601_date


def localtime_to_utc(date, l_date_format="%Y%m%d%H%M%S", l_timezone='Asia/Shanghai',
                     r_date_format="%Y-%m-%dT%H:%M:%S.%fZ"):
    utc_date = datetime.datetime.strptime(date, l_date_format).replace(tzinfo=pytz.timezone(l_timezone)).astimezone(
        pytz.timezone('UTC'))
    utc_date = utc_date.strftime(r_date_format)
    return utc_date


def utc_to_localtime(date, l_date_format="%Y-%m-%dT%H:%M:%S.%fZ", l_timezone='Asia/Shanghai',
                     r_date_format="%Y%m%d%H%M%S"):
    local_date = datetime.datetime.strptime(date, l_date_format).replace(tzinfo=pytz.timezone('UTC')).astimezone(
        pytz.timezone(l_timezone))
    localtime = local_date.strftime(r_date_format)
    return localtime


def timestamp_to_datetime(timestamp):
    return datetime.datetime.fromtimestamp(timestamp)


def datetime_to_timestamp(date_string, date_format):
    """
    This function converts dates with format for python 2.x
    'Thu Jul 13 08:22:34 2017' to seconds since 1970. "%a %b %d %H:%M:%S %Y"
    time data '03/30/20 18:49:04' does match format '%m/%d/%y %H:%M:%S'
    in Python 3.x can get same result by 'datetime.datetime.timestamp()'
    """
    return time.mktime(datetime.datetime.strptime(date_string, date_format).timetuple())


def is_datetime_newer(l_date, r_date, date_format):
    """
    is left datetime newer than right datetime
    :param l_date: date_string in date_format
    :param r_date: date_string in date_format
    :param date_format: such as '%m/%d/%y %H:%M:%S'
    :return: boolean
    """
    return datetime.datetime.strptime(l_date, date_format) > datetime.datetime.strptime(r_date, date_format)


def is_between_datetime(date_string, l_date, r_date, date_format):
    """
    is date_string between l_date and r_date
    :param date_string: date_string in date_format
    :param l_date: date_string in date_format
    :param r_date: date_string in date_format
    :param date_format: such as '%m/%d/%y %H:%M:%S'
    :return: boolean
    """
    is_left = datetime.datetime.strptime(l_date, date_format) <= datetime.datetime.strptime(date_string, date_format)
    is_right = datetime.datetime.strptime(date_string, date_format) < datetime.datetime.strptime(r_date, date_format)
    return is_left and is_right


if __name__ == '__main__':
    print(get_days_between_two_date("20200325", "20200402"))
    print(localtime_to_utc_iso8601("20200301091400", l_date_format="%Y%m%d%H%M%S"))
    print(localtime_to_utc_iso8601("20200326091400", l_date_format="%Y%m%d%H%M%S"))
    print(timestamp_to_datetime(1583107200))
    print(utc_to_localtime("2020-03-26T01:08:00.000000Z", ))
    print(localtime_to_utc_iso8601("20200326091400", r_date_format="%Y-%m-%d %H:%M:%S.%fZ"))
    print(utc_to_localtime("20200624131754Z", l_date_format="%Y%m%d%H%M%SZ"))
