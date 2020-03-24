#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created by PyCharm.
File Name:              LinuxBashShellScriptForOps:watch-http-server-status.py
Version:                0.0.1
Author:                 dgden
Author Email:           dgdenterprise@gmail.com
URL:                    https://github.com/DingGuodong/LinuxBashShellScriptForOps
Download URL:           https://github.com/DingGuodong/LinuxBashShellScriptForOps/tarball/master
Create Date:            2020/3/23
Create Time:            12:14
Description:            watcher for http web server, keep doing request until 'ok' is returned
Long Description:       
References:             
Prerequisites:          pip install requests
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


def get_http_request(url):
    querystring = {}
    headers = {
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/77.0.3865.90 Safari/537.36",
        'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;"
                  "q=0.8,application/signed-exchange;v=b3",
        'Accept-Language': "en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7,zh-TW;q=0.6,mt;q=0.5",
        'cache-control': "no-cache",
        'Connection': "close"
    }

    try:
        response = requests.request("GET", url, headers=headers, params=querystring, timeout=30)
        if response.ok:
            return response.ok, response.status_code
        else:
            return response.ok, response.status_code
    except requests.exceptions.ConnectionError:
        # current request is too fast that may be banned with 'Max retries exceeded with url'
        print("WARN, try again after few seconds ...")
        time.sleep(round(random.uniform(20, 30), 0))
    except requests.exceptions.ReadTimeout:
        print("WARN, timeout, try again after few seconds ...")

    return False, -1


def http_server_watcher(url):
    while 1:
        is_ok, status_code = get_http_request(url)
        if not is_ok:
            print(time.strftime("%Y/%m/%d %H:%M:%S"), "Fail", status_code)
        else:
            print(time.strftime("%Y/%m/%d %H:%M:%S"), "Ok", status_code)
            break


if __name__ == '__main__':
    http_server_watcher("https://zhihu.com/")
