# -*- coding:utf-8 -*-
import os
import time
import datetime
import sys

try:
    import ntplib
except ImportError:
    try:
        command_to_execute = "pip install ntplib"
        os.system(command_to_execute)
    except OSError:
        exit(1)
    finally:
        import ntplib

tz = time.strftime("%Z", time.localtime(time.time())).decode(encoding=sys.getfilesystemencoding()).encode('utf-8')
print "当前时区 ==> %s" % tz

server = 'pool.ntp.org'  # time.nist.gov  time-nw.nist.gov

c = ntplib.NTPClient()
r = c.request(server)
t = r.tx_time

time_in_server = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(t))
time_in_local = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
if r.offset > 15:
    print "当前系统时间 => %s" % time_in_local
    print "服务器时间 => %s" % time_in_server
