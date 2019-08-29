#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
Created by PyCharm.
File:               LinuxBashShellScriptForOps:retrieveLatestOpenSSLVersionUrl.py
User:               Guodong
Create Date:        2017/3/7
Create Time:        14:25

retrieve, fetch, find latest version of PCRE URL

 """

import re

import requests
from bs4 import BeautifulSoup

headers = {
    'Cache-Control': 'max-age=0',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) \
    Chrome/54.0.2840.99 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'DNT': '1',
    'Accept-Encoding': 'gzip, deflate, sdch',
    'Accept-Language': 'en-US,en;q=0.8,zh-CN;q=0.6,zh-TW;q=0.4'
}

downloads_page_url = 'http://zlib.net/'
file_url_list = list()
latest_version = ""
file_url = ""

content = requests.get(downloads_page_url, headers=headers)
Soup = BeautifulSoup(content.text, 'lxml')
available_version = Soup.find_all('a')

for link in available_version:
    pattern = re.compile(r'zlib-.*\.tar\.gz$')
    match = pattern.search(link.get("href"))
    if match:
        file_url_list.append(downloads_page_url + match.group())

print(file_url_list[0])
