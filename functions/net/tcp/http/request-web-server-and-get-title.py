#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created by PyCharm.
File Name:              LinuxBashShellScriptForOps:request-web-server-and-get-title.py
Version:                0.0.1
Author:                 dgden
Author Email:           dgdenterprise@gmail.com
URL:                    https://github.com/DingGuodong/LinuxBashShellScriptForOps
Download URL:           https://github.com/DingGuodong/LinuxBashShellScriptForOps/tarball/master
Create Date:            2020/05/26
Create Time:            10:27
Description:            request a web server and get title
Long Description:
                        response  # <class 'requests.models.Response'>
                        response.content.decode("utf-8")
                        response.text.encode(response.encoding).decode("utf-8"))
References:             
Prerequisites:          pip3 install requests
Development Status:     3 - Alpha, 5 - Production/Stable
Environment:            Console
Intended Audience:      System Administrators, Developers, End Users/Desktop
License:                Freeware, Freely Distributable
Natural Language:       English, Chinese (Simplified)
Operating System:       POSIX :: Linux, Microsoft :: Windows
Programming Language:   Python :: 2.7
Topic:                  Utilities
Note:                   str in python3 is same to unicode in python2, unicode of Python2 is equivalent to str in Python
 """
import re

import requests


def get_title_from_html(text):
    """
    also can use 'lxml' or 'BeautifulSoup'
    :param text:
    :type text: str
    :return:
    :rtype: str
    """
    pattern = re.compile('<title>(.*?)</title>')
    match = pattern.search(text)
    if match:
        groups_tuple = match.groups()
        return groups_tuple[0]
    else:
        return text


def request_ip_port_80(ip):
    """
    request a url with redirect
    :return:
    """
    url = 'http://{}/'.format(ip)

    try:
        response = requests.request('GET', url, allow_redirects=True, timeout=(2.0, 2.0))
    except requests.exceptions.ConnectTimeout:
        print("{} : {}".format(ip, "connect timeout"))
        return False
    except requests.exceptions.ReadTimeout:
        print("{} : {}".format(ip, "read timeout"))
        return False
    except requests.exceptions.SSLError:
        print("{} : {}".format(ip, "ssl error"))
        return False
    except requests.exceptions.ConnectionError:
        print("{} : {}".format(ip, "connection failed"))
        return False

    if response.ok:
        # response.content type: bytes
        print("{} : {}".format(ip, get_title_from_html(str(response.content))))
        # print("{} : {}".format(ip, get_title_from_html(response.content.decode("utf-8").encode("utf-8"))))

        # response.text    type: unicode
        print("{} : {}".format(ip, get_title_from_html(str(response.text.encode(response.encoding)))))
        return True
    else:
        return False


if __name__ == '__main__':
    request_ip_port_80("192.168.88.142")
