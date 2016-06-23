#!/usr/bin/python
# -*- coding: utf-8 -*-
# Do not reinventing the wheel
import urllib2
import urllib

find = dict()
find['wd'] = "python"
s = "https://www.baidu.com/s"
wd = urllib.urlencode(find)
url = s + "?" + wd
req = urllib2.Request(url)
req.add_header('User-Agent',
               "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.84 Safari/537.36")
resp = urllib2.urlopen(req)
print resp.read()
