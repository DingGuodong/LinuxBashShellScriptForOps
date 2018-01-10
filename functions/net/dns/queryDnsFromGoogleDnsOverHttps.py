#!/usr/bin/python
# encoding: utf-8
# -*- coding: utf8 -*-
"""
Created by PyCharm.
File:               LinuxBashShellScriptForOps:queryDnsFromGoogleDnsOverHttps.py
User:               Guodong
Create Date:        2017/1/3
Create Time:        11:22
 """
import json
import sys

import requests


# GoogleDnsOverHttps = "https://dns.google.com/resolve?name="
# GoogleDnsOverHttpsHumanFriendly = "https://dns.google.com/query?name="

def google_public_dns_query(name):
    url = "https://dns.google.com/resolve"

    querystring = {"name": name}

    headers = {
        'cache-control': "no-cache",
    }

    proxies = {
        "http": "http://127.0.0.1:1080",
        "https": "http://127.0.0.1:1080",  # Note: key in dict must be lower case
    }

    data = ""

    try:
        # Pass a (connect, read) timeout tuple, or a single float to set both timeouts to the same value
        response = requests.request("GET", url, headers=headers, params=querystring, proxies=proxies, timeout=(10, 5))
        if response.ok:
            data = response.text.strip()
    except Exception as _:
        print _
        print _.args
        print _.message
        sys.exit(1)

    # example response data:
    # {"Status": 0,"TC": false,"RD": true,"RA": true,"AD": false,"CD": false,
    # "Question":[ {"name": "www.taobao.com.","type": 1}],
    # "Answer":[ {"name": "www.taobao.com.","type": 5,"TTL": 421,"data": "www.taobao.com.danuoyi.tbcache.com."},
    # {"name": "www.taobao.com.danuoyi.tbcache.com.","type": 1,"TTL": 59,"data": "58.216.17.103"},
    # {"name": "www.taobao.com.danuoyi.tbcache.com.","type": 1,"TTL": 59,"data": "58.218.215.155"}],
    # "Comment": "Response from 203.107.0.100"}

    response_data_json = data
    response_data_dict = json.loads(response_data_json)
    answer_raw_list = response_data_dict['Answer']
    answer_ip_list = list()
    for item in answer_raw_list:
        if item['type'] == 1:
            answer_ip_list.append(item['data'])
    return answer_ip_list


if __name__ == '__main__':
    print google_public_dns_query("www.taobao.com")
