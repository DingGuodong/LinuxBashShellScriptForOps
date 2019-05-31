#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import sys
import urllib.request, urllib.parse, urllib.error
import urllib.request, urllib.error, urllib.parse
import json
import datetime

grant_type = None
appid = None
secret = None

lock = ".wechat_lock"
if not os.path.exists(lock):
    o = open(lock, 'w')
    o.write("")
    o.close()

content = None
content_length = None
if os.path.exists(lock):
    o = open(lock, 'r')
    content = o.read()
    content_length = len(content)
    o.close()

if content_length != 0:
    content_dict = json.loads(content)
    expire_time = content_dict['expires_on']
    expire_time = datetime.datetime.strptime(expire_time, '%Y-%m-%d %H:%M:%S.%f')
    now_time = datetime.datetime.now()
    if now_time < expire_time:
        print("The token is not empty, and token is %s" % content_dict['access_token'])
        print("The token will expire on %s" % content_dict['expires_on'])
        exit(1)

argc = len(sys.argv)
if not (argc == 1 or argc == 3):
    print("Error: incorrect number of arguments or unrecognized option")
if argc == 1:
    grant_type = "client_credential"
    appid = "wxe200ced8ed4adc3f"
    secret = "a88e01c2962501229ae4eeb58902d44e"
else:
    if sys.argv[1] is not None and sys.argv[2] is not None and sys.argv[3] is not None:
        grant_type = sys.argv[1]
        appid = sys.argv[2]
        secret = sys.argv[3]

parameters = {
    "grant_type": grant_type,
    "appid": appid,
    "secret": secret
}

url_parameters = urllib.parse.urlencode(parameters)

token_url = "https://api.weixin.qq.com/cgi-bin/token?"
url = token_url + url_parameters
response = urllib.request.urlopen(url)
returns = response.read()
c = json.loads(returns)
if c['access_token'] is not None:
    print("access_token is: %s" % c['access_token'])
    print("expires_in is: %s" % c['expires_in'])
    if os.path.exists(lock):
        get_time = datetime.datetime.now()
        expire_time = get_time + datetime.timedelta(seconds=c['expires_in'])
        c['expires_on'] = str(expire_time)
        o = open(lock, "w")
        content_new = json.dumps(c)
        o.write(content_new)
        o.close()
else:
    if c['errcode'] is not None:
        print("errcode is: %s" % c['errcode'])
        print("errmsg is: %s" % c['errmsg'])
        if os.path.exists(lock):
            os.remove(lock)
    else:
        print(returns)
