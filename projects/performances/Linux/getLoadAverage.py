#!/usr/bin/python
# encoding: utf-8
# -*- coding: utf8 -*-

import os
import sys
import time

try:
    import psutil
except ImportError:
    try:
        command_to_execute = "pip install psutil"
        os.system(command_to_execute)
    except OSError:
        print "failed install psutil"
        sys.exit(1)
finally:
    import psutil

boot_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(psutil.boot_time()))
print "system start at: %s" % boot_time
print "now: %s" % time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))

uptime_total_seconds = time.time() - psutil.boot_time()
uptime_days = int(uptime_total_seconds / 24 / 60 / 60)
uptime_hours = int(uptime_total_seconds / 60 / 60 % 24)
uptime_minutes = int(uptime_total_seconds / 60 % 60)
uptime_seconds = int(uptime_total_seconds % 60)
print "uptime: %d days %d hours %d minutes %d seconds" % (uptime_days, uptime_hours, uptime_minutes, uptime_seconds)

user_number = len(psutil.users())
print "%d user:" % user_number
print "\t\\"
for user_tuple in psutil.users():
    user_name = user_tuple[0]
    user_terminal = user_tuple[1]
    user_host = user_tuple[2]
    user_login_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(user_tuple[3]))
    print "\t|- user online: %s, login from %s with terminal %s at %s" % (
    user_name, user_host, user_terminal, user_login_time)

cpu_count = psutil.cpu_count()
try:
    with open('/proc/loadavg', 'r') as f:
        loadavg_c = f.read().split(' ')
        loadavg = dict()
        if loadavg_c is not None:
            loadavg['lavg_1'] = loadavg_c[0]
            loadavg['lavg_5'] = loadavg_c[1]
            loadavg['lavg_15'] = loadavg_c[2]
            loadavg['nr'] = loadavg_c[3]
            loadavg['last_pid'] = loadavg_c[4]
    print "load average: %s, %s, %s" % (loadavg['lavg_1'], loadavg['lavg_5'], loadavg['lavg_15'])
    if loadavg['lavg_15'] > cpu_count:
        print "Note: cpu 15 min load is high!"
    if loadavg['lavg_5'] > cpu_count:
        print "Note: cpu 5 min load is high!"
    if loadavg['lavg_1'] > cpu_count:
        print "Note: cpu 1 min load is high!"
except IOError:
    pass
