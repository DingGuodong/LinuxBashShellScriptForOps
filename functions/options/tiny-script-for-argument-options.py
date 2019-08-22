#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created by PyCharm.
File Name:              LinuxBashShellScriptForOps:tiny-script-for-argument-options.py
Version:                0.0.1
Author:                 dgden
Author Email:           dgdenterprise@gmail.com
URL:                    https://github.com/DingGuodong/LinuxBashShellScriptForOps
Download URL:           https://github.com/DingGuodong/LinuxBashShellScriptForOps/tarball/master
Create Date:            2019/8/22
Create Time:            10:01
Description:            an tiny example for argument options without getopt or docopt
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
from sys import argv


def check_if_equal_any(string, iterable):
    """
    return True if any item of iterable equal to string
    :param string: str obj
    :param iterable: iterable obj such as list/tuple etc.
    :return: boolean
    """
    return any(map(lambda item: item == string, iterable))


def check_if_in_any(string, iterable):
    """
    return True if any item of iterable in string
    :param string: str obj
    :param iterable: iterable obj such as list/tuple etc.
    :return: boolean
    """
    return any(map(lambda item: item in string, iterable))


def check_if_in_all(string, iterable):
    """
    return True if all item of iterable in string
    :param string: str obj
    :param iterable: iterable obj such as list/tuple etc.
    :return: boolean
    """
    return all(map(lambda item: item in string, iterable))


def help():
    print("help msg")


def main_entrypoint():
    print("main_process msg")


if __name__ == '__main__':
    if any([check_if_equal_any(x, ['-h', '--help']) for x in argv]) or len(argv) < 2:  # only 1 extra para is required
        help()
        exit(1)
    else:
        main_entrypoint()
