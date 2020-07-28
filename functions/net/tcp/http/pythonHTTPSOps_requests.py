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


def requests_example1():
    """
    request a common URL
    :return:
    """
    # http://docs.python-requests.org/en/master/
    # http://docs.python-requests.org/en/master/user/quickstart/#make-a-request
    r = requests.get('https://api.github.com/user', auth=('user', 'pass'))
    print r.status_code
    print r.headers['content-type']
    print r.encoding
    print r.text.encode(r.encoding)
    print r.content.decode(r.encoding)
    print r.json()


def requests_example2():
    """
    request a url with redirect
    :return:
    """
    url_with_302_307 = 'http://www.baidu.com/'
    response = requests.request('GET', url_with_302_307, allow_redirects=True)  # Defaults to ``True``.
    print(response.status_code)
    print(response.encoding)
    if response.ok:
        print(response.text.encode(response.encoding))


def requests_example3():
    """
    request a URL with a valid cert authority
    :return:
    """
    try:
        from requests.packages import urllib3
    except ImportError:
        import urllib3
    urllib3.disable_warnings()  # equal to import logging; logging.captureWarnings(capture=True)

    url_with_ssl_issue = 'https://dgd2010.blog.51cto.com/'
    response = requests.request('GET', url_with_ssl_issue, verify=False, allow_redirects=False)
    print(response.status_code)
    print(response.encoding)


def requests_post_example_1():
    url = 'https://51devops.com/httpbin/anything'
    data = {
        'key1': 'value1',
        'key2': 'value2',
        'key3': 'value3',
    }
    res = requests.post(url, data)
    if res.ok:
        print res.content
    else:
        print res.status_code
        print res.content


if __name__ == '__main__':
    requests_post_example_1()
