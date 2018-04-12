#!/usr/bin/python
# encoding: utf-8
# -*- coding: utf8 -*-
"""
Created by PyCharm.
File Name:              LinuxBashShellScriptForOps:pyStrToDatetime.py
Version:                0.0.1
Author:                 Guodong
Author Email:           dgdenterprise@gmail.com
URL:                    https://github.com/DingGuodong/LinuxBashShellScriptForOps
Download URL:           https://github.com/DingGuodong/LinuxBashShellScriptForOps/tarball/master
Create Date:            2018/4/8
Create Time:            19:41
Description:            convert string obj to datetime obj(learn from 'python-whois')
Long Description:       bug fix for 'whois' module although this is not best solution
References:             https://github.com/gen1us2k/python-whois/issues/21
                        https://github.com/gen1us2k/python-whois/blob/master/whois/_3_adjust.py
                        https://github.com/DannyCork/python-whois/blob/master/whois/_3_adjust.py
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
import re
import sys

PYTHON_VERSION = sys.version_info[0]

# http://docs.python.org/library/datetime.html#strftime-strptime-behavior
DATE_FORMATS = [
    '%d-%b-%Y',  # 02-jan-2000
    '%d.%m.%Y',  # 02.02.2000
    '%d/%m/%Y',  # 01/06/2011
    '%Y-%m-%d',  # 2000-01-02
    '%Y.%m.%d',  # 2000.01.02
    '%Y/%m/%d',  # 2005/05/30
    '%d-%m-%Y',  # 31-01-2000
    '%m-%d-%Y',  # 01-31-2000
    '%Y. %m. %d.',  # 2000. 01. 31. (Korean style)
    '%b-%Y',  # aug-1996 (very old uk domains)

    '%Y.%m.%d %H:%M:%S',  # 2002.09.19 13:00:00
    '%Y%m%d %H:%M:%S',  # 20110908 14:44:51
    '%Y-%m-%d %H:%M:%S',  # 2011-09-08 14:44:51
    '%d.%m.%Y  %H:%M:%S',  # 19.09.2002 13:00:00
    '%d-%b-%Y %H:%M:%S %Z',  # 24-Jul-2009 13:20:03 UTC
    '%d %b %Y %H:%M %Z',
    '%Y/%m/%d %H:%M:%S (%z)',  # 2011/06/01 01:05:01 (+0900)
    '%Y/%m/%d %H:%M:%S',  # 2011/06/01 01:05:01
    '%a %b %d %H:%M:%S %Z %Y',  # Tue Jun 21 23:59:59 GMT 2011
    '%a %b %d %H:%M:%S %Y',  # Tue Jun 21 23:59:59 2015
    '%a %b %d %Y',  # Tue Dec 12 2000
    '%Y-%m-%dT%H:%M:%S',  # 2007-01-26T19:10:31
    '%Y-%m-%dT%H:%M:%SZ',  # 2007-01-26T19:10:31Z
    '%Y-%m-%dT%H:%M:%S %z',  # 2011-03-30T19:36:27+0200
    '%Y-%m-%dT%H:%M:%S.%f %z',  # 2011-09-08T14:44:51.622265+03:00
    '%Y-%m-%dt%H:%M:%S.%f',  # 2011-09-08t14:44:51.622265
]


def str_to_date_py2_my(s):
    tmp = re.findall('[+-]([0-9]{2})00', s)
    if tmp:
        tz = int(tmp[0])
    else:
        tz = 0

    if s.count("-") > 2:
        add = False
    else:
        add = True

    if tz != 0:
        s = "-".join(re.split('[+-]', s)[:-1])

    for date_format in DATE_FORMATS:
        try:
            if add:
                # return UTC time
                return datetime.datetime.strptime(s, date_format) - datetime.timedelta(hours=tz)
            else:
                # return UTC time
                return datetime.datetime.strptime(s, date_format) + datetime.timedelta(hours=tz)
        except ValueError:
            pass

    raise ValueError("Unknown date format: '%s'" % s)


def str_to_date_py2_my_u1(s):
    tmp = re.findall('[+-]([0-9]{2})00', s)
    if tmp:
        tz = int(tmp[0])
    else:
        tz = 0

    if s.count("-") > 2:
        tz = -tz

    if tz != 0:
        s = "-".join(re.split('[+-]', s)[:-1])

    for date_format in DATE_FORMATS:
        try:
            return datetime.datetime.strptime(s, date_format) - datetime.timedelta(hours=tz)
        except ValueError:
            pass

    raise ValueError("Unknown date format: '%s'" % s)


def str_to_date_py2_gen1us2k(s):
    """
    https://github.com/gen1us2k/python-whois
    https://github.com/gen1us2k/python-whois/blob/master/whois/_3_adjust.py
    :param s:
    :return:
    """
    tmp = re.findall('\s([+-][0-9]{2})00', s)
    if tmp:
        tz = int(tmp[0][1])
    else:
        tz = 0

    s = re.sub('\s\([+-]([0-9]{2})([0-9]{2})\)', '', s)
    s = re.sub('\s[+-]([0-9]{2})([0-9]{2})', '', s)

    for format in DATE_FORMATS:
        try:
            return datetime.datetime.strptime(s, format) + datetime.timedelta(hours=tz)
        except ValueError as e:
            pass

    raise ValueError("Unknown date format: '{0}'".format(s))


def str_to_date_py2_DannyCork(s):
    """
    https://github.com/DannyCork/python-whois
    https://github.com/DannyCork/python-whois/blob/master/whois/_3_adjust.py
    :param s: 
    :return: 
    """
    tmp = re.findall('\+([0-9]{2})00', s)
    if tmp:
        tz = int(tmp[0])
    else:
        tz = 0

    for format in DATE_FORMATS:
        try:
            return datetime.datetime.strptime(s, format) + datetime.timedelta(hours=tz)
        except ValueError as e:
            pass

    raise ValueError("Unknown date format: '%s'" % s)


if __name__ == '__main__':
    print(str_to_date_py2_my('2026-10-11T00:00:00-0700'))  # this time format from 'whois' command, `whois baidu.com`
    print(str_to_date_py2_my('2026-10-11T15:00:00+0800'))

    print(str_to_date_py2_my_u1('2026-10-11T00:00:00-0700'))
    print(str_to_date_py2_my_u1('2026-10-11T15:00:00+0800'))

    print(str_to_date_py2_gen1us2k('2026-10-11T00:00:00 (-0700)'))
    print(str_to_date_py2_gen1us2k('2026-10-11T15:00:00 (+0800)'))

    print(str_to_date_py2_DannyCork('2026-10-11T00:00:00 (-0700)'))
    print(str_to_date_py2_DannyCork('2026-10-11T00:00:00 (+0800)'))
