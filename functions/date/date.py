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
