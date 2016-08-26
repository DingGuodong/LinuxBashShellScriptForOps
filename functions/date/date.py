# encoding: utf-8
# -*- coding: utf8 -*-
import time
import datetime
import sys

system_encoding = sys.getfilesystemencoding()
print "Current system encoding is \"%s\"." % system_encoding

print time.strftime("%Y-%m-%d %H:%M:%S %Z").decode(system_encoding).encode("utf-8")

i = datetime.datetime.now()
print str(i)
print i.strftime('%Y/%m/%d %H:%M:%S')
print ("%s" % i.isoformat())

# Get Unix timestamp
print time.time()

# Unix timestamp to Time
print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(1471932539.15))

# Time to Unix timestamp
print time.mktime(time.strptime('2016-08-23 14:08:01', '%Y-%m-%d %H:%M:%S'))
