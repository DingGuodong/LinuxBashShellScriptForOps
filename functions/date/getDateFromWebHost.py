# -*- coding:utf-8 -*-
import urllib2
import datetime
import time
import os

host = 'https://www.baidu.com'
request = urllib2.Request(host)
response = urllib2.urlopen(request)
date = response.info().getheader('Date')
print date
# Thu, 16 Jun 2016 01:49:52 GMT
# https://docs.python.org/2/library/datetime.html#strftime-and-strptime-behavior
time_header = datetime.datetime.strptime(date, '%a, %d %b %Y %H:%M:%S %Z')

# print time.strptime(date, '%a, %d %b %Y %H:%M:%S %Z')

print time_header

print datetime.datetime.now()

time_tuple = time.mktime(time_header.timetuple())
print time.strftime('%Y-%m-%d %H:%M:%S', time_header.timetuple())
