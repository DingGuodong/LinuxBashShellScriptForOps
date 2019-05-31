#!/usr/bin/python
# encoding: utf-8
# -*- coding: utf8 -*-
"""
Created by PyCharm.
File:               LinuxBashShellScriptForOps:picklingWithPickle.py
User:               Guodong
Create Date:        2017/6/14
Create Time:        15:28
 """

try:
    import cPickle as pickle
except ImportError:
    import pickle

import requests

url = "http://coolshell.cn/feed"

payload = ""
headers = {
    'cache-control': "no-cache",
}

response = requests.request("GET", url, data=payload, headers=headers)

xml_text = response.text

with open('somefile', 'wb') as f:
    pickle.dump(xml_text, f)

with open('somefile', 'rb') as f:
    print(pickle.load(f))
