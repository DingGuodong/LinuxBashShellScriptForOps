# encoding: utf-8
# -*- coding: utf8 -*-
import calendar
import sys

import datetime
import delorean
import pytz
import time
from dateutil.relativedelta import relativedelta  # pip install -U python-dateutil

# Define the constants
SECONDS_PER_MINUTE = 60
SECONDS_PER_HOUR = 3600
SECONDS_PER_DAY = 86400

# 'Wed Feb 14 09:25:49 2018'
print(time.asctime())
# local structure time
print(time.localtime())
# GMT structure time
print(time.gmtime())

# Convert seconds into GMT date
print(time.strftime("%a, %d %b %Y %H:%M:%S +0000", time.gmtime(time.time())))

# Python's program to get current time MST EST UTC GMT HST


mst = pytz.timezone('MST')
print("Time in MST:", datetime.datetime.now(mst))

est = pytz.timezone('EST')
print("Time in EST:", datetime.datetime.now(est))

utc = pytz.timezone('UTC')
print("Time in UTC:", datetime.datetime.now(utc))

gmt = pytz.timezone('GMT')
print("Time in GMT:", datetime.datetime.now(gmt))

hst = pytz.timezone('HST')
print("Time in HST:", datetime.datetime.now(hst))

print(time.strftime('%Y%m%d%H%M%S', time.localtime(time.time())))
print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))

print(time.strftime('%Y-%m-%d %H:%M:%S', time.strptime("20170416145604.489009+480".split(".")[0], '%Y%m%d%H%M%S')))

# week number of year, with Monday as first day of week (00..53), For Linux, command is 'date +%W'
print(time.strftime("%W"))
print(time.strftime("%W", time.localtime(time.mktime(time.strptime('2017/11/30', '%Y/%m/%d')))))

system_encoding = sys.getfilesystemencoding()
print("Current system encoding is \"%s\"." % system_encoding)

print(time.strftime("%Y-%m-%d %H:%M:%S %Z").decode(system_encoding).encode("utf-8"))

i = datetime.datetime.now()
print(str(i))
print(i.strftime('%Y/%m/%d %H:%M:%S'))
print("%s" % i.isoformat())

GMT_FORMAT = '%b %d %H:%M:%S %Y GMT'
print(datetime.datetime.utcnow().strftime(GMT_FORMAT))

# Get Unix timestamp
print(time.time())
print(time.mktime(time.strptime("2018-05-23 23:59:59", "%Y-%m-%d %H:%M:%S")))
print(time.mktime((datetime.datetime.now() - datetime.timedelta(days=3 * 30)).timetuple()))
print(time.mktime((datetime.datetime.strptime("2018-05-23 23:59:59", "%Y-%m-%d %H:%M:%S") - datetime.timedelta(
    days=3 * 30)).timetuple()))

# Unix timestamp to Time
print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(1471932539.15)))
print(datetime.datetime.fromtimestamp(1471932539.15).strftime("%Y-%m-%d %H:%M"))
print(datetime.datetime.fromtimestamp(1471932539.15, pytz.timezone('Asia/Shanghai')).strftime('%Y-%m-%d %H:%M:%S %Z%z'))

# Time to Unix timestamp
print(time.mktime(time.strptime('2016-08-23 14:08:01', '%Y-%m-%d %H:%M:%S')))
# # Saturday, October 10, 2015 10:10:00 AM
# year, month, day, hour=None, minute=None, second=None, microsecond=None, tzinfo=None
print("Unix Timestamp: ", (time.mktime(datetime.datetime(2015, 10, 10, 10, 10).timetuple())))

# Time zone support
print(delorean.Delorean(timezone="Asia/Shanghai"))
print(delorean.Delorean(timezone="Asia/Shanghai").datetime)
print(delorean.Delorean(timezone="Asia/Shanghai").epoch)
print(delorean.Delorean(timezone="Asia/Shanghai").date)
print(delorean.Delorean(timezone="Asia/Shanghai").start_of_day)
print(delorean.Delorean(timezone="Asia/Shanghai").end_of_day)

# 20161229235959Z, Z代表0时区，或者叫UTC统一时间。

# refers to http://www.pythonprogramming.in/date-time.html
# Python's program to calculate time difference between two datetime objects.
datetimeFormat = '%Y-%m-%d %H:%M:%S.%f'
date1 = '2016-04-16 10:01:28.585'
date2 = '2016-03-10 09:56:28.067'
diff = datetime.datetime.strptime(date1, datetimeFormat) \
       - datetime.datetime.strptime(date2, datetimeFormat)
print("Difference:", diff)
print("Days:", diff.days)
print("Microseconds:", diff.microseconds)
print("Seconds:", diff.seconds)

# Python's program to display all dates between two dates.
start = datetime.datetime.strptime("2016-05-30", "%Y-%m-%d")
end = datetime.datetime.strptime("2016-06-02", "%Y-%m-%d")
date_array = \
    (start + datetime.timedelta(days=x) for x in range(0, (end - start).days))
for date_object in date_array:
    print(date_object.strftime("%Y-%m-%d"))

# Python's program to add N year month day hour min sec to date.
add_days = datetime.datetime.today() + relativedelta(days=+6)
add_months = datetime.datetime.today() + relativedelta(months=+6)
add_years = datetime.datetime.today() + relativedelta(years=+6)
add_hours = datetime.datetime.today() + relativedelta(hours=+6)
add_mins = datetime.datetime.today() + relativedelta(minutes=+6)
add_seconds = datetime.datetime.today() + relativedelta(seconds=+6)
print("Current Date Time:", datetime.datetime.today())
print("Add 6 days:", add_days)
print("Add 6 months:", add_months)
print("Add 6 years:", add_years)
print("Add 6 hours:", add_hours)
print("Add 6 mins:", add_mins)
print("Add 6 seconds:", add_seconds)

# Python's program to subtract N year month day hour min sec to date.
sub_days = datetime.datetime.today() + relativedelta(days=-6)
sub_months = datetime.datetime.today() + relativedelta(months=-6)
sub_years = datetime.datetime.today() + relativedelta(years=-6)
sub_hours = datetime.datetime.today() + relativedelta(hours=-6)
sub_mins = datetime.datetime.today() + relativedelta(minutes=-6)
sub_seconds = datetime.datetime.today() + relativedelta(seconds=-6)
print("Current Date Time:", datetime.datetime.today())
print("Subtract 6 days:", sub_days)
print("Subtract 6 months:", sub_months)
print("Subtract 6 years:", sub_years)
print("Subtract 6 hours:", sub_hours)
print("Subtract 6 mins:", sub_mins)
print("Subtract 6 seconds:", sub_seconds)

# Python's program to weekday of first day of the month and
# number of days in month, for the specified year and month.
print("Year:2002 - Month:2")
month_range = calendar.monthrange(2002, 2)
print("Weekday of first day of the month:", month_range[0])
print("Number of days in month:", month_range[1])
print()
print("Year:2010 - Month:5")
month_range = calendar.monthrange(2010, 5)
print("Weekday of first day of the month:", month_range[0])
print("Number of days in month:", month_range[1])

# Conversion between different types
timestamp = 1226527167.595983
date_str = "2008-11-13 17:53:59.595983"
nginx_time_local = '08/Jan/2018:12:05:20 +0800'  # "%d/%b/%Y:%H:%M:%S %z"

# mysql timezone setting
# [mysqld]
# log_timestamps = SYSTEM
# default-time_zone = '+8:00'
mysql_query_general_log_time = '2019-10-15T10:25:40.829852Z'  # "%Y-%m-%dT%H:%M:%S.%fZ"

time_tuple = (2008, 11, 13, 5, 59, 27, 3, 318, 0)
dt_obj = datetime.datetime(2008, 11, 13, 5, 59, 27, 595983)
# timestamp to time tuple(time obj)
time.localtime(timestamp)
time.gmtime(timestamp)
# timestamp to datetime(datetime obj)
datetime.datetime.fromtimestamp(timestamp)

# string to time tuple(time obj), precision lost
time.strptime(date_str, "%Y-%m-%d %H:%M:%S.%f")
# string to datetime(datetime obj)
datetime.datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S.%f")

# print time with timezone
# timetuple(time.struct_time) -->float(timestamp) --> datetime.datetime with timezone
print(datetime.datetime.fromtimestamp(
    time.mktime(time.strptime(nginx_time_local[:-6], "%d/%b/%Y:%H:%M:%S")),
    pytz.timezone('Asia/Shanghai')).strftime('%Y-%m-%d %H:%M:%S %z'))

print(datetime.datetime.fromtimestamp(
    time.mktime(datetime.datetime.strptime(nginx_time_local[:-6], "%d/%b/%Y:%H:%M:%S").timetuple()),
    pytz.timezone('Asia/Shanghai')).strftime('%Y-%m-%d %H:%M:%S %z'))

# mysql time to nginx time
# mysql time in CST
print(datetime.datetime.strptime(mysql_query_general_log_time, "%Y-%m-%dT%H:%M:%S.%fZ").strftime(
    '"%d/%b/%Y:%H:%M:%S %z"'))
# mysql time in UTC
print((datetime.datetime.strptime(mysql_query_general_log_time, "%Y-%m-%dT%H:%M:%S.%fZ") + (
        datetime.datetime.now() - datetime.datetime.utcnow())).strftime('"%d/%b/%Y:%H:%M:%S %z"'))
# mysql time in UTC, match nginx time well
print(datetime.datetime.strptime(mysql_query_general_log_time, "%Y-%m-%dT%H:%M:%S.%fZ").replace(
    tzinfo=pytz.timezone('UTC')).astimezone(pytz.timezone('Asia/Shanghai')).strftime('"%d/%b/%Y:%H:%M:%S %z"'))
# python get current timezone and get the time difference from UTC
# python获取当前时区并计算与UTC的时间差
print(datetime.datetime.now(pytz.timezone('Asia/Shanghai')))
# datetime.datetime(2019, 10, 16, 10, 58, 41, 860000, tzinfo=<DstTzInfo 'PRC' CST+8:00:00 STD>)
# 2019-10-16 10:58:41.860000+08:00
print(datetime.datetime.now(pytz.timezone('PRC')))
# datetime.datetime(2019, 10, 16, 2, 58, 51, 119000, tzinfo=<UTC>)
# 2019-10-16 02:58:51.119000+00:00
print(datetime.datetime.now(pytz.timezone('UTC')))

assert datetime.datetime.now(pytz.timezone('PRC')) == datetime.datetime.now(pytz.timezone('UTC'))

print((datetime.datetime.now() - datetime.datetime.utcnow()).seconds / 3600)

# time tuple(time obj) to string, precision lost
time.strftime("%Y-%m-%d %H:%M:%S", time_tuple)  # <type 'str'>, '2008-11-13 05:59:27'
# time tuple(time obj) to timestamp, precision lost
time.mktime(time_tuple)  # <type 'float'>, 1226527167.0
# time tuple(time obj) to datetime(datetime obj), precision lost
datetime.datetime(*time_tuple[0:6])  # <type 'datetime.datetime'>, datetime.datetime(2008, 11, 13, 5, 59, 27)

# datetime(datetime obj) to time tuple(time obj), precision lost
dt_obj.timetuple()
# datetime(datetime obj) to string
dt_obj.strftime("%Y-%m-%d %H:%M:%S.%f")  # <type 'str'>, '2008-11-13 05:59:27.595983'
# datetime(datetime obj) can not to timestamp

# UTC time('Z' letter in string) convert to another timezone
datetime.datetime.strptime('2018-06-07T10:57:14Z', "%Y-%m-%dT%H:%M:%SZ").replace(
    tzinfo=pytz.timezone('UTC')).astimezone(pytz.timezone('Asia/Shanghai'))

# others
# Time delta operation and convert to str object
print((datetime.datetime.now() + datetime.timedelta(days=158)).strftime("%Y-%m-%d %H:%M:%S.%f"))

# get timestamp before n days
save_days = 30
timestamp_before_save_days = time.mktime((datetime.datetime.today() + relativedelta(days=-save_days)).timetuple())
print(timestamp_before_save_days)

# how many days between datetime A and datetime B
print(
    (datetime.datetime.strptime('2018-10-15', "%Y-%m-%d") - datetime.datetime.strptime('2018-08-29', "%Y-%m-%d")).days)
print((datetime.datetime.now() - datetime.datetime.strptime('2019-05-09', "%Y-%m-%d")).days)
