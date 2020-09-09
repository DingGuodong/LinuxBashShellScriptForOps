#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created by PyCharm.
File Name:              LinuxBashShellScriptForOps:requests-get-file-content.py
Version:                0.0.1
Author:                 dgden
Author Email:           dgdenterprise@gmail.com
URL:                    https://github.com/DingGuodong/LinuxBashShellScriptForOps
Download URL:           https://github.com/DingGuodong/LinuxBashShellScriptForOps/tarball/master
Create Date:            2020/9/8
Create Time:            17:21
Description:            get file's content using requests
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
import requests


def get_file_content(url):
    headers = {
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/77.0.3865.90 Safari/537.36",
        'Accept': "*/*",
        'Accept-Language': "en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7,zh-TW;q=0.6,mt;q=0.5",
        'cache-control': "no-cache",
        'Connection': "close"
    }

    try:
        response = requests.request('GET', url, headers=headers, allow_redirects=True, timeout=(10.0, 10.0))
        if response.ok:
            return response.content  # type: bytes
        else:
            return b''

    except requests.exceptions.ConnectTimeout:
        print("{} : {}".format(url, "connect timeout"))
    except requests.exceptions.ReadTimeout:
        print("{} : {}".format(url, "read timeout"))
    except requests.exceptions.SSLError:
        print("{} : {}".format(url, "ssl error"))
    except requests.exceptions.ConnectionError:
        print("{} : {}".format(url, "connection failed"))

    return b''


if __name__ == '__main__':
    cur_url = 'http://update.cz88.net/soft/setup.zip'
    file_content = get_file_content(cur_url)

    if file_content:
        with open("setup.zip", 'wb') as fp:
            fp.write(file_content)
