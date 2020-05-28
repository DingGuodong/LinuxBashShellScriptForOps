#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created by PyCharm.
File Name:              LinuxBashShellScriptForOps:python-get-html-tag.py
Version:                0.0.1
Author:                 dgden
Author Email:           dgdenterprise@gmail.com
URL:                    https://github.com/DingGuodong/LinuxBashShellScriptForOps
Download URL:           https://github.com/DingGuodong/LinuxBashShellScriptForOps/tarball/master
Create Date:            2020/5/28
Create Time:            10:52
Description:            using bs4 to get html tag
Long Description:       
References:             
Prerequisites:          pip install beautifulsoup4
                        pip install requests
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
import bs4
import requests
from bs4 import BeautifulSoup

url = 'http://bbs.fengniao.com/forum/11022712.html'

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/83.0.4103.61 Safari/537.36',
    'Accept': "text/html, application/xhtml+xml, image/jxr, */*",
    'Accept-Encoding': "gzip, deflate",
    'Accept-Language': 'zh-Hans-CN, zh-Hans; q=0.5',  # en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7,zh-TW;q=0.6,mt;q=0.5
}

try:
    response = requests.request("GET", url, headers=headers)
except requests.exceptions.ConnectTimeout as e:
    print(url, e)
except requests.exceptions.ReadTimeout as e:
    print(url, e)
except requests.exceptions.SSLError as e:
    print(url, e)
except requests.exceptions.ConnectionError as e:
    print(url, e)
else:
    if response.ok:
        wanted_html = response.text

        soup = BeautifulSoup(wanted_html, 'lxml')

        wanted_div_tag_list = soup.find_all("div", attrs={'class': 'img'})

        for wanted_div_tag in wanted_div_tag_list:  # type: bs4.element.Tag
            print(wanted_div_tag.find("img").get("src"))
