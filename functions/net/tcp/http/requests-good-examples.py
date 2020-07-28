#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created by PyCharm.
File Name:              LinuxBashShellScriptForOps:requests-good-examples.py
Version:                0.0.1
Author:                 dgden
Author Email:           dgdenterprise@gmail.com
URL:                    https://github.com/DingGuodong/LinuxBashShellScriptForOps
Download URL:           https://github.com/DingGuodong/LinuxBashShellScriptForOps/tarball/master
Create Date:            2019/10/9
Create Time:            12:45
Description:            good examples of requests
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

import random

import requests
import time


def sleep_random_seconds(start=20, end=30):
    time.sleep(round(random.uniform(start, end), 0))


def sleep_random_seconds_float(start=0, end=1):
    time.sleep(random.uniform(start, end))


# useful for web spider stuff
def keep_request_until_success(method, url, headers=None, data=None, params=None):
    """

    :param method: GET or POST
    :type method: str
    :param url: URL
    :type url: str
    :param headers:
    :type headers: dict
    :param data: POST data
    :type data: dict
    :param params: GET params
    :type params: dict
    :return: content
    :rtype: bytes
    """
    if headers is None:
        headers = {
            'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/77.0.3865.90 Safari/537.36",
            'Accept': "*/*",
            'Accept-Language': "en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7,zh-TW;q=0.6,mt;q=0.5",
            'cache-control': "no-cache",
            'Connection': "close"
        }

    content = b""
    while 1:
        # Tips: 如果requests长期卡住，则可能表明网络存在异常，如网络不稳定，DNS无法解析等等，
        # 比如DNS解析异常会导致urllib卡住进而导致requests卡住，有个不错的临时解决办法是把网断开再连接。
        # 参考链接：
        # https://blog.csdn.net/pilipala6868/article/details/80712195
        # https://www.v2ex.com/t/365351
        # https://www.cnblogs.com/niansi/p/7143736.html
        try:
            response = requests.request(method, url, headers=headers, params=params, data=data, timeout=30)
        except requests.exceptions.ConnectionError:
            # current request is too fast that may be banned with 'Max retries exceeded with url'
            print("WARN, try again after few seconds ...")
            sleep_random_seconds()
            continue
        except requests.exceptions.ReadTimeout:
            print("WARN, timeout, try again after few seconds ...")
            continue
        if response.ok:
            content = response.content
            break

    return content
