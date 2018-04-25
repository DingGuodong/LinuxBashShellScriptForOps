# -*- coding:utf-8 -*-
import os
import time
# import datetime
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

mswindows = (sys.platform == "win32")  # learning from 'subprocess' module
linux = (sys.platform == "linux2")

tz = time.strftime("%Z", time.localtime(time.time())).decode(encoding=sys.getfilesystemencoding()).encode('utf-8')
print "当前时区 ==> %s" % tz

server = 'pool.ntp.org'  # time.nist.gov  time-nw.nist.gov

c = ntplib.NTPClient()
r = c.request(server)
t = r.tx_time  # Transmit timestamp in system time.

time_in_server = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(t))
time_in_local = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
if r.offset > 15:
    print "当前系统时间与服务器时间相差15s以上"
    print "当前系统时间 => %s" % time_in_local
    print "服务器时间 => %s" % time_in_server
    # setting system date and time
    _date = time.strftime('%Y-%m-%d', time.localtime(t))
    _time = time.strftime('%X', time.localtime(t))
    if mswindows:
        os.system('date {} && time {}'.format(_date, _time))
    elif linux:
        os.system("date -s \"%s %s\" && hwclock -w" % (_date, _time))
    else:
        print("你也许现在想修改系统时间")
