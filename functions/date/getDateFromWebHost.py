# -*- coding:utf-8 -*-
import datetime
import time

import requests

ws_host_url = 'https://www.jd.com/'
date = requests.get(ws_host_url).headers.get("date")

print(date)  # Thu, 16 Jun 2016 01:49:52 GMT

time_header = datetime.datetime.strptime(date, '%a, %d %b %Y %H:%M:%S %Z')  # <class 'datetime.datetime'>

print(time_header.now())  # <class 'datetime.datetime'>
print(time.strftime('%Y-%m-%d %H:%M:%S', time_header.now().timetuple()))
print(time.strftime('%Y-%m-%d %H:%M:%S', time.strptime(date, '%a, %d %b %Y %H:%M:%S %Z')))

print(time_header.now().timetuple())
print(time.strptime(date, '%a, %d %b %Y %H:%M:%S %Z'))
