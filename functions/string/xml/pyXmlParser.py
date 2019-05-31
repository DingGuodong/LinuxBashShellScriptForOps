#!/usr/bin/python
# encoding: utf-8
# -*- coding: utf8 -*-
"""
Created by PyCharm.
File:               LinuxBashShellScriptForOps:pyXmlParser.py
User:               Guodong
Create Date:        2017/6/14
Create Time:        14:04
 """

try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET

import requests

import os

tmp_xml_file = 'tmp_xml_file.xml'  # this file will auto created and auto deleted during running

url = "http://coolshell.cn/feed"

payload = ""
headers = {
    'cache-control': "no-cache",
}

response = requests.request("GET", url, data=payload, headers=headers)

xml_text = response.text

with open(tmp_xml_file, 'wb') as f:
    f.write(xml_text.encode('utf-8'))

tree = ET.ElementTree(file=tmp_xml_file)

# Ref: http://codingpy.com/article/parsing-xml-using-python/
# 查找需要的元素, 通过XPath查找元素
for elem in tree.iterfind('channel/title'):
    print(elem.tag, elem.attrib, elem.text, end=' ')

os.remove(tmp_xml_file)
