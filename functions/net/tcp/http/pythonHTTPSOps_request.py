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


def example1():
    # http://docs.python-requests.org/en/master/
    # http://docs.python-requests.org/en/master/user/quickstart/#make-a-request
    r = requests.get('https://api.github.com/user', auth=('user', 'pass'))
    print r.status_code
    print r.headers['content-type']
    print r.encoding
    print r.text.encode(r.encoding)
    print r.json()


def example2():
    url_with_302_307 = 'http://www.baidu.com/'
    response = requests.request('GET', url_with_302_307, allow_redirects=True)  # Defaults to ``True``.
    print(response.status_code)
    print(response.encoding)
    if response.ok:
        print(response.text.encode(response.encoding))


if __name__ == '__main__':
    example2()
