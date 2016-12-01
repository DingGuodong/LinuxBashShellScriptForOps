# encoding: utf-8
# -*- coding: utf8 -*-
import time
import datetime
import sys
import delorean

system_encoding = sys.getfilesystemencoding()
print "Current system encoding is \"%s\"." % system_encoding

print time.strftime("%Y-%m-%d %H:%M:%S %Z").decode(system_encoding).encode("utf-8")

i = datetime.datetime.now()
print str(i)
print i.strftime('%Y/%m/%d %H:%M:%S')
print ("%s" % i.isoformat())

GMT_FORMAT = '%b %d %H:%M:%S %Y GMT'
print datetime.datetime.utcnow().strftime(GMT_FORMAT)

# Get Unix timestamp
print time.time()

# Unix timestamp to Time
print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(1471932539.15))
print datetime.datetime.fromtimestamp(1471932539.15).strftime("%Y-%m-%d %H:%M")

# Time to Unix timestamp
print time.mktime(time.strptime('2016-08-23 14:08:01', '%Y-%m-%d %H:%M:%S'))

# Time zone support
print delorean.Delorean(timezone="Asia/Shanghai")
print delorean.Delorean(timezone="Asia/Shanghai").datetime
print delorean.Delorean(timezone="Asia/Shanghai").epoch
print delorean.Delorean(timezone="Asia/Shanghai").date
print delorean.Delorean(timezone="Asia/Shanghai").start_of_day
print delorean.Delorean(timezone="Asia/Shanghai").end_of_day

# 20161229235959Z, Z代表0时区，或者叫UTC统一时间。
