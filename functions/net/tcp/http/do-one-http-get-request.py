#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created by PyCharm.
File Name:              LinuxBashShellScriptForOps:do-one-http-get-request.py
Version:                0.0.1
Author:                 dgden
Author Email:           dgdenterprise@gmail.com
URL:                    https://github.com/DingGuodong/LinuxBashShellScriptForOps
Download URL:           https://github.com/DingGuodong/LinuxBashShellScriptForOps/tarball/master
Create Date:            2020/7/28
Create Time:            17:16
Description:            do one HTTP GET request
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
import requests


def do_one_http_get_request(url):
    headers = {
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/77.0.3865.90 Safari/537.36",
        'Accept': "*/*",
        'Accept-Language': "en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7,zh-TW;q=0.6,mt;q=0.5",
        'cache-control': "no-cache",
        'Connection': "close"
    }
    try:
        response = requests.request('GET', url, headers=headers, timeout=10.0)
        if response.ok:
            return True
        else:
            return False
    except requests.exceptions.ConnectionError:
        return False
    except requests.exceptions.ReadTimeout:
        return False
