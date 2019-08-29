#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
Created by PyCharm.
File:               LinuxBashShellScriptForOps:zabbix-monitor-json-api.py
User:               Guodong
Create Date:        2017/1/6
Create Time:        11:00
 """

# demo: HTTP API => Filesystem API
# Basic procedure:
# 1. get json data from API Server using http client(pycurl, urllib, request, etc) and save data to persistent storage
# this step require a standalone py script to request data and save data,
# persistent storage can be Redis, Database or Filesystem.
# 2. get specified data for Monitor Service(such as Zabbix), using passing different parameters to the script.
# this step using this py script(reading data from Filesystem storage)

import os
import sys
import json


def usage():
    print("""Usage:  %s [key_name]

check health with json style API
""" % __file__)


if len(sys.argv) != 2:
    print("syntax error, this script accepts one argument. but %d argument(s) received." % (len(sys.argv) - 1))
    usage()
    sys.exit(1)

api_url = r"monitor-afms.json"  # Note: using absolutely path is required
if not os.path.exists(api_url):
    print("API test failed, can not read API service file")
    sys.exit(1)

with open(api_url, 'r') as f:
    result = json.loads(f.read())

if result['errcode'] == 0:
    print(0)
else:
    if sys.argv[1] in result['errmsg'].keys():
        if result['errmsg'][sys.argv[1]]['code'] != 0:
            print(1)
        else:
            print(0)
    else:
        print("""argument error, this script accepts argument(s):
%s,
but \"%s\" argument received.
""" % (result['errmsg'].keys(), sys.argv[1]))
        sys.exit(1)
