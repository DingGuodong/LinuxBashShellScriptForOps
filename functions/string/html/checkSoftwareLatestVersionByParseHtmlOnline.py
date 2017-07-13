#!/usr/bin/python
# encoding: utf-8
# -*- coding: utf8 -*-
"""
Created by PyCharm.
File:               LinuxBashShellScriptForOps:checkSoftwareLatestVersionByParseHtmlOnline.py
User:               Guodong
Create Date:        2017/7/13
Create Time:        13:53
Description:        check software(CentOS) latest version by parse HTML online
References:         
 """
import requests
from bs4 import BeautifulSoup
import prettytable
import os
import re

url_to_check = r'https://www.centos.org/download/'

headers = {
    'Cache-Control': 'max-age=0',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'DNT': '1',
    'Accept-Encoding': 'gzip, deflate, sdch',
    'Accept-Language': 'en-US,en;q=0.8,zh-CN;q=0.6,zh-TW;q=0.4'
}

resource = requests.get(url_to_check, headers=headers)
Soup = BeautifulSoup(resource.text, 'lxml')
download_list = Soup.find('div', class_="downloadbutton").find_all('a')

table = prettytable.PrettyTable(border=True, header=True, left_padding_width=2, padding_width=1)
table.field_names = ["Name", "Filename", "Version", "Download URL"]

for item in download_list:
    title = item.get_text().replace(u' ', ' ')  # Note: prettytable only support ASCII code
    href = item['href']
    filename = os.path.basename(href)
    version = filename.split('-')[-1].split('.')[0]

    pattern = re.compile(r'-(\d+)\.iso')
    match = pattern.search(filename)
    if match:
        version = match.group(1)

    table.add_row([title, filename, version, href])

for field in table.field_names:
    table.align[field] = "l"
print table
