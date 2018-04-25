# -*- coding:utf-8 -*-
import urllib2
import datetime
import time
import certifi

host = 'https://www.baidu.com'
request = urllib2.Request(host)
response = urllib2.urlopen(request, timeout=10, cafile=certifi.where())  # socket.setdefaulttimeout(10)
date = response.info().getheader('Date')

print(date)  # Thu, 16 Jun 2016 01:49:52 GMT

# https://docs.python.org/2/library/datetime.html#strftime-and-strptime-behavior
time_header = datetime.datetime.strptime(date, '%a, %d %b %Y %H:%M:%S %Z')

print(time_header.now())

print(time.strftime('%Y-%m-%d %H:%M:%S', time_header.now().timetuple()))
