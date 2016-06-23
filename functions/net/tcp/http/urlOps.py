# -*- coding: utf8 -*-
import urllib2

url = u"http://www.baidu.com/?wd=测试"
print urllib2.urlopen(url.encode('utf-8')).read()
