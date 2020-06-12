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
Programming Language:   Python :: 3
Topic:                  Utilities
 """

import random
import time

import requests


# useful for web spider stuff
def keep_request_until_success():
    url = "http://res.example.com/xxx/xxx"
    querystring = {
        "id": "xxx",
        "num": "xxx"
    }
    headers = {
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/77.0.3865.90 Safari/537.36",
        'Referer': "http://res.example.com/xxx",
        'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;"
                  "q=0.8,application/signed-exchange;v=b3",
        'Accept-Language': "en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7,zh-TW;q=0.6,mt;q=0.5",
        'cache-control': "no-cache",
        'Connection': "close"
    }

    text = ""
    while 1:
        # Tips: 如果requests长期卡住，则可能表明网络存在异常，如网络不稳定，DNS无法解析等等，
        # 比如DNS解析异常会导致urllib卡住进而导致requests卡住，有个不错的临时解决办法是把网断开再连接。
        # 参考链接：
        # https://blog.csdn.net/pilipala6868/article/details/80712195
        # https://www.v2ex.com/t/365351
        # https://www.cnblogs.com/niansi/p/7143736.html
        try:
            response = requests.request("GET", url, headers=headers, params=querystring, timeout=30)
        except requests.exceptions.ConnectionError:
            # current request is too fast that may be banned with 'Max retries exceeded with url'
            print("WARN, try again after few seconds ...")
            time.sleep(round(random.uniform(20, 30), 0))
            continue
        except requests.exceptions.ReadTimeout:
            print("WARN, timeout, try again after few seconds ...")
            continue
        if response.ok:
            text = response.text
            break

    return text
