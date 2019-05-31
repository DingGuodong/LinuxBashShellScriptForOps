#!/usr/bin/python
# encoding: utf-8
# -*- coding: utf8 -*-
"""
Created by PyCharm.
File Name:              LinuxBashShellScriptForOps:getPublicIPAddress_requestsImpl.py
Version:                0.0.1
Author:                 Guodong
Author Email:           dgdenterprise@gmail.com
URL:                    https://github.com/DingGuodong/LinuxBashShellScriptForOps
Download URL:           https://github.com/DingGuodong/LinuxBashShellScriptForOps/tarball/master
Create Date:            2018/1/9
Create Time:            17:30
Description:            python get public ip address by requests library through Internet network access
Long Description:       
References:
                        https://ifconfig.co/
                        http://ip.taobao.com/service/getIpInfo.php?ip=113.200.54.58&qq-pf-to=pcqq.group

Prerequisites:          requests
Development Status:     3 - Alpha, 5 - Production/Stable
Environment:            Console
Intended Audience:      System Administrators, Developers, End Users/Desktop
License:                Freeware, Freely Distributable
Natural Language:       English, Chinese (Simplified)
Operating System:       POSIX :: Linux, Microsoft :: Windows
Programming Language:   Python :: 3
Topic:                  Utilities
 """
import sys

import requests


def get_public_address_from_site_ifconfig():
    query_ip_api_url = 'https://ifconfig.co/ip'

    headers = {
        'Cache-Control': "no-cache",
    }

    data = ""

    try:
        # Pass a (connect, read) timeout tuple, or a single float to set both timeouts to the same value
        response = requests.request("GET", query_ip_api_url, headers=headers, timeout=(10, 5))
        if response.ok:
            data = response.text.strip()
    except Exception as _:
        # print _
        # print _.args
        # print _.message
        del _

    return data


def get_ip_information_from_site_ifconfig():
    query_ip_api_url = 'https://ifconfig.co/json'

    headers = {
        'Cache-Control': "no-cache",
    }

    data = ""

    try:
        # Pass a (connect, read) timeout tuple, or a single float to set both timeouts to the same value
        response = requests.request("GET", query_ip_api_url, headers=headers, timeout=(10, 5))
        if response.ok:
            data = response.text.strip()
    except Exception as e:
        print(e)

    return data


def get_ip_information_from_site_taobao(ip):
    if ip == '':
        sys.exit(1)

    query_ip_api_url = "http://ip.taobao.com/service/getIpInfo.php"

    querystring = {"ip": ip}

    headers = {
        'Cache-Control': "no-cache",
    }

    data = ""

    try:
        # Pass a (connect, read) timeout tuple, or a single float to set both timeouts to the same value
        response = requests.request("GET", query_ip_api_url, headers=headers, params=querystring, timeout=(5, 5))
        if response.ok:
            data = response.text.strip()
    except Exception as e:
        print(e)

    return data


if __name__ == '__main__':
    public_ip_address = get_public_address_from_site_ifconfig()
    print(public_ip_address)
    print(get_ip_information_from_site_ifconfig())
    print(get_ip_information_from_site_taobao(public_ip_address))
