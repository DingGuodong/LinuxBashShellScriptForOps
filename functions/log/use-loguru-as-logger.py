#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created by PyCharm.
File Name:              LinuxBashShellScriptForOps:use-loguru-as-logger.py
Version:                0.0.1
Author:                 dgden
Author Email:           dgdenterprise@gmail.com
URL:                    https://github.com/DingGuodong/LinuxBashShellScriptForOps
Download URL:           https://github.com/DingGuodong/LinuxBashShellScriptForOps/tarball/master
Create Date:            2020/9/18
Create Time:            11:37
Description:            using loguru make logging simple and stupid
Long Description:       loguru is python3 module make logging simple and stupid
References:             [loguru](https://github.com/Delgan/loguru)
Prerequisites:          pip3.8 install loguru
Development Status:     3 - Alpha, 5 - Production/Stable
Environment:            Console
Intended Audience:      System Administrators, Developers, End Users/Desktop
License:                Freeware, Freely Distributable
Natural Language:       English, Chinese (Simplified)
Operating System:       POSIX :: Linux, Microsoft :: Windows
Programming Language:   Python :: 3
Topic:                  Utilities
 """

import sys

from loguru import logger

logger.add(sys.stderr, format="{time} {level} {message}", filter="__main__", level="INFO")

logger.info("If you're using Python {}, prefer {feature} of course!", 3.6, feature="f-strings")


@logger.catch
def my_function(x):
    # An error? It's caught anyway!
    return 1 / x


if __name__ == '__main__':
    my_function(0)
