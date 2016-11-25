#!/usr/bin/python
# encoding: utf-8
# -*- coding: utf8 -*-
"""
Created by PyCharm.
File:               LinuxBashShellScriptForOps:pythonHTTPSOps3.py
User:               Guodong
Create Date:        2016/11/23
Create Time:        11:40
 """
import requests

# http://docs.python-requests.org/en/master/
# http://docs.python-requests.org/en/master/user/quickstart/#make-a-request
r = requests.get('https://api.github.com/user', auth=('user', 'pass'))
print r.status_code
print r.headers['content-type']
print r.encoding
print r.text
print r.json()
