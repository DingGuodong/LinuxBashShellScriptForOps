# -*- coding: utf8 -*-
import urllib.request, urllib.error, urllib.parse

url = "http://www.baidu.com/?wd=测试"
print(urllib.request.urlopen(url.encode('utf-8')).read())
