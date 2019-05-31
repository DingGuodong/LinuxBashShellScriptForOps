# -*- coding:utf-8 -*-
import locale
import os
# import datetime
import sys
import time

try:
    import ntplib
except ImportError:
    try:
        command_to_execute = "pip3 install ntplib"
        os.system(command_to_execute)
    except OSError:
        exit(1)
    finally:
        import ntplib

mswindows = (sys.platform == "win32")  # learning from 'subprocess' module
linux = (sys.platform == "linux2")

encoding = locale.getpreferredencoding()
tz = time.tzname[0].encode("iso-8859-1").decode(encoding)
print("当前时区 ==> %s" % tz)

server = 'pool.ntp.org'  # time.nist.gov  time-nw.nist.gov

c = ntplib.NTPClient()
r = c.request(server)
t = r.tx_time  # Transmit timestamp in system time.

time_in_server = time.strftime("%Y-%m-%d %H:%M:%S %z", time.localtime(t))
time_in_local = time.strftime("%Y-%m-%d %H:%M:%S %z", time.localtime(time.time()))
print(time_in_local, time_in_server, sep="\n")

if r.offset > 15:
    print("当前系统时间与服务器时间相差15s以上")
    print("当前系统时间 => %s" % time_in_local)
    print("服务器时间 => %s" % time_in_server)
    # setting system date and time
    _date = time.strftime('%Y-%m-%d', time.localtime(t))
    _time = time.strftime('%X', time.localtime(t))
    if mswindows:
        os.system('date {} && time {}'.format(_date, _time))
    elif linux:
        os.system("date -s \"%s %s\" && hwclock -w" % (_date, _time))
    else:
        print("你也许现在想修改系统时间")
