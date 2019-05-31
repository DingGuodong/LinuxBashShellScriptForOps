#!/usr/bin/python
# encoding: utf-8
# -*- coding: utf8 -*-
"""
Created by PyCharm.
File Name:              LinuxBashShellScriptForOps:pyGetAppInfoFromTencentAppStore.py
Version:                0.0.1
Author:                 Guodong
Author Email:           dgdenterprise@gmail.com
URL:                    https://github.com/DingGuodong/LinuxBashShellScriptForOps
Download URL:           https://github.com/DingGuodong/LinuxBashShellScriptForOps/tarball/master
Create Date:            2018/1/4
Create Time:            18:16
Description:            get app info from Tencent App Store using requests + re
Long Description:       
References:             
Prerequisites:          []
Development Status:     3 - Alpha, 5 - Production/Stable
Environment:            Console
Intended Audience:      System Administrators, Developers, End Users/Desktop
License:                Freeware, Freely Distributable
Natural Language:       English, Chinese (Simplified)
Operating System:       POSIX :: Linux, Microsoft :: Windows
Programming Language:   Python :: 3

Topic:                  Utilities
 """

import re

import requests

apk_name = "com.tencent.mm"  # http://sj.qq.com/myapp/search.htm?kw=微信

url = "http://sj.qq.com/myapp/detail.htm"

querystring = {"apkName": apk_name}

headers = {
    'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/63.0.3239.108 Safari/537.36",
    'Cache-Control': "no-cache",
}

response = requests.request("GET", url, headers=headers, params=querystring)

page_content = response.text
# print response.headers
# print response.headers['Set-Cookie']  # requests will help you save cookies in header and send cookies header

appDetailData_json = None
pattern = re.compile('var appDetailData *= *({[^{}]*\})')  # get json like data from java scripts
match = pattern.search(page_content)
if match:
    appDetailData = match.groups()[0]
    if appDetailData:
        re_item = re.compile(r'(?<=[\s,])\w+')  # format json like data to real json data in Python
        appDetailData_json = re_item.sub("\"\g<0>\"", appDetailData)

if appDetailData_json:
    print(appDetailData_json.replace('\t', "    "))
    # print json.dumps(json.loads(appDetailData_json), indent=4)
