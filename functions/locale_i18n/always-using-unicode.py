#!/usr/bin/python
# encoding: utf-8
# -*- coding: utf-8 -*-
"""
Created by PyCharm.
File Name:              LinuxBashShellScriptForOps:always-using-unicode.py
Version:                0.0.1
Author:                 Guodong
Author Email:           dgdenterprise@gmail.com
URL:                    https://github.com/DingGuodong/LinuxBashShellScriptForOps
Download URL:           https://github.com/DingGuodong/LinuxBashShellScriptForOps/tarball/master
Create Date:            2018/9/27
Create Time:            18:49
Description:            a function convert non-unicode object to unicode object if it is a basestring object
Long Description:       
References:             https://coolshell.cn/articles/461.html
                        http://farmdev.com/talks/unicode/
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


def to_unicode_or_bust(obj, encoding='utf-8'):
    """
    convert non-unicode object to unicode object
    :param obj: str object or unicode
    :param encoding:
    :return:
    """
    if isinstance(obj, basestring):
        if not isinstance(obj, unicode):
            obj = unicode(obj, encoding)

    return obj


def to_str_or_bust(obj, encoding='utf-8'):
    """
    convert unicode object to str object
    :param obj: unicode object or str
    :param encoding:
    :return:
    """
    if isinstance(obj, basestring):
        if isinstance(obj, unicode):
            obj = obj.encode(encoding)

    return obj


# an example for encoding or decoding
def remove(path, ending, recursive=False):  # Unicode everywhere
    import os

    path = to_unicode_or_bust(path)  # Decode early
    ending = to_unicode_or_bust(ending)  # Decode early

    for top, dirs, nondirs in os.walk(path):
        for _file in nondirs:
            file_to_deal = os.path.join(top, _file)
            if file_to_deal.endswith(ending) and os.path.exists(file_to_deal):
                """
                A bad example here:
                Path() (from pathlib import Path) is only accepting str object more than unicode object,
                so Path()..exist() method is no better than os.path.exists(), using os.path.exists() instead
                """
                try:
                    print("%s is deleted." % file_to_deal)
                    os.remove(file_to_deal)
                except IOError as e:
                    print(e)
                    print(e.args)
                    print(e.message)
        if not recursive:
            break


if __name__ == '__main__':
    work_dir = r"D:\tmp\培训课程\linux培训视频（持续更新）xxxx a very long path here balabala " \
               r"\linux基础命令-20160308-mp4"
    remove(work_dir, ending="副本.mp4")
    # for the next: Encode late
    # print "ok好".decode("utf-8").encode("gbk")
