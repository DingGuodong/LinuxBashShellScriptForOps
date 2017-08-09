#!/usr/bin/python
# encoding: utf-8
# -*- coding: utf8 -*-
"""
Created by PyCharm.
File:               LinuxBashShellScriptForOps:checkIfInBlockLists.py
User:               Guodong
Create Date:        2017/8/9
Create Time:        11:39
Description:        check if domain name or ip in block lists
References:         
 """
import requests
from bs4 import BeautifulSoup


def bl_urlbl(domain):
    url = "https://admin.uribl.com/"

    querystring = {"section": "lookup"}

    payload = "------WebKitFormBoundary7MA4YWxkTrZu0gW\r\n" \
              "Content-Disposition: form-data; name=\"domains\"\r\n\r\n{domains}\r\n" \
              "------WebKitFormBoundary7MA4YWxkTrZu0gW\r\n" \
              "Content-Disposition: form-data; name=\"section\"\r\n\r\nlookup\r\n" \
              "------WebKitFormBoundary7MA4YWxkTrZu0gW\r\n" \
              "Content-Disposition: form-data; name=\"method\"\r\n\r\n\r\n" \
              "------WebKitFormBoundary7MA4YWxkTrZu0gW--".format(domains=domain)
    headers = {
        'content-type': "multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW",
        'referer': "https://admin.uribl.com/?section=lookup",
        'cache-control': "no-cache",
        'postman-token': "f4a0f3d0-6589-af06-f1cb-a4648600afdf"
    }

    response = requests.request("POST", url, data=payload, headers=headers, params=querystring)

    soup = BeautifulSoup(response.text, 'lxml')
    lookup_results = soup.find('table', class_="lookup_form").find_all('span')
    for item in lookup_results:
        if item['title'] != '':
            return item['title']


def bl_spamhaus():
    # https://www.spamhaus.org/query/ip/124.129.14.90, need JavaScript support
    pass


if __name__ == '__main__':
    domain_name = "example.com"
    print bl_urlbl(domain_name)
