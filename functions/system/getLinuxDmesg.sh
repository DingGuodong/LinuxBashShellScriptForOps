#!/bin/sh
# Refer to: http://blog.csdn.net/wzb56_earl/article/details/50625705
uptime_ts=`cat /proc/uptime | awk '{ print $1}'`
dmesg | awk -v uptime_ts=${uptime_ts} 'BEGIN {
    now_ts = systime();
    start_ts = now_ts - uptime_ts;
    #print "system start time seconds:", start_ts;
    #print "system start time:", strftime("[%Y/%m/%d %H:%M:%S]", start_ts);
}
{
    print strftime("[%Y/%m/%d %H:%M:%S]", start_ts + substr($1, 2, length($1) - 2)), $0
}'