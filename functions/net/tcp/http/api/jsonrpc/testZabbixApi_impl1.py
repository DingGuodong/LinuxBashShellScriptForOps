#!/usr/bin/python
# -*- coding: utf-8 -*-
# Do not reinventing the wheel
import cookielib
import urllib2
import urllib
import json

# https://www.zabbix.com/documentation/3.0/manual/config/items/itemtypes/zabbix_agent

username = "Admin"
password = "Pc608qq2Cd"

# first url request
zabbixBaseUrl = "https://ops.huntor.cn/"
cookie = cookielib.CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
urllib2.install_opener(opener)
urllib2.urlopen(zabbixBaseUrl)

for item in cookie:
    print item

# second time do url request, the CookieJar will auto handle the cookie
authUrl = zabbixBaseUrl + "api_jsonrpc.php"

para_dict_authentication = {
    "jsonrpc": "2.0",
    "method": "user.login",
    "params": {
        "user": username,
        "password": password
    },
    "id": 1,
    "auth": None
}

para_json_authentication = json.dumps(para_dict_authentication)

para_authentication = para_json_authentication

# postData = urllib.urlencode(para_authentication)

postData = para_authentication

req = urllib2.Request(authUrl,
                      postData)
req.add_header('User-Agent',
               'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.84 Safari/537.36')
req.add_header('Content-Type', 'application/json-rpc')
req.add_header('Cache-Control', 'no-cache')
req.add_header('Accept', '*/*')
req.add_header('Connection', 'Keep-Alive')
resp = urllib2.urlopen(req)
respInfo = resp.info()
respRead = resp.read()

print respInfo

print respRead

respRead_dict = json.loads(respRead)

print respRead_dict

print "Authentication token is: %s" % respRead_dict['result']
