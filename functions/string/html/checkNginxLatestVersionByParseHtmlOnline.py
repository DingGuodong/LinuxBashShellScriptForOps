#!/usr/bin/python
# encoding: utf-8
# -*- coding: utf8 -*-
"""
Created by PyCharm.
File:               LinuxBashShellScriptForOps:checkNginxLatestVersionByParseHtmlOnline.py
User:               Guodong
Create Date:        2017/7/13
Create Time:        17:12
Description:        check software(Nginx) latest version by parse HTML online
References:         https://www.crummy.com/software/BeautifulSoup/bs4/doc/
                    https://www.crummy.com/software/BeautifulSoup/bs4/doc.zh/


 """
import requests
from bs4 import BeautifulSoup
import prettytable
import os
import re

url_to_check = r'http://nginx.org/en/download.html'


def get_base_url(url):
    import urllib.request, urllib.parse, urllib.error
    import urllib.parse
    proto, rest = urllib.parse.splittype(url)
    res, rest = urllib.parse.splithost(rest)
    return urllib.parse.urlunsplit((proto, res, "", "", ""))


def join_url(base, path):
    import urllib.request, urllib.parse, urllib.error
    return urllib.basejoin(base, path)


headers = {
    'Cache-Control': 'max-age=0',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/54.0.2840.99 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'DNT': '1',
    'Accept-Encoding': 'gzip, deflate, sdch',
    'Accept-Language': 'en-US,en;q=0.8,zh-CN;q=0.6,zh-TW;q=0.4'
}

resource = requests.get(url_to_check, headers=headers)
Soup = BeautifulSoup(resource.text, 'lxml')
download_list = Soup.find('div', id="content").find_all('a')
for num, item in enumerate(download_list):
    if num == 6:  # latest nginx stable version location
        title = item.get_text()
        href = item['href']
        filename = os.path.basename(href)
        pattern = re.compile(r'-([\d.]+)\.tar')
        match = pattern.search(filename)
        if match:
            version = match.group(1)

table = prettytable.PrettyTable(border=True, header=True, left_padding_width=2, padding_width=1)
table.field_names = ["Name", "Filename", "Version", "Download URL"]
table.add_row([title, filename, version, join_url(get_base_url(url_to_check), href)])
for field in table.field_names:
    table.align[field] = "l"
print(table)
