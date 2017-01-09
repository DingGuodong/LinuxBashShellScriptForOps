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
import requests
import json

GoogleDnsOverHttps = "https://dns.google.com/resolve?name="
GoogleDnsOverHttpsHumanFriendly = "https://dns.google.com/query?name="

url = "https://dns.google.com/resolve"

querystring = {"name": "www.taobao.com"}

headers = {
    'cache-control': "no-cache",
}

response = requests.request("GET", url, headers=headers, params=querystring)

print response.text

# example response data:
# {"Status": 0,"TC": false,"RD": true,"RA": true,"AD": false,"CD": false,
# "Question":[ {"name": "www.taobao.com.","type": 1}],
# "Answer":[ {"name": "www.taobao.com.","type": 5,"TTL": 421,"data": "www.taobao.com.danuoyi.tbcache.com."},
# {"name": "www.taobao.com.danuoyi.tbcache.com.","type": 1,"TTL": 59,"data": "58.216.17.103"},
# {"name": "www.taobao.com.danuoyi.tbcache.com.","type": 1,"TTL": 59,"data": "58.218.215.155"}],
# "Comment": "Response from 203.107.0.100"}

response_data_json = response.text
response_data_dict = json.loads(response_data_json)
answer_raw_list = response_data_dict['Answer']
answer_ip_list = list()
for item in answer_raw_list:
    if item['type'] == 1:
        answer_ip_list.append(item['data'])
print answer_ip_list
