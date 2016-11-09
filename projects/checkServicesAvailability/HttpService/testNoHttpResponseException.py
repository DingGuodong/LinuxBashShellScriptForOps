#!/usr/bin/python
# encoding: utf-8
# -*- coding: utf8 -*-
"""
Created by PyCharm.
File:               LinuxBashShellScriptForOps:testNoHttpResponseException,testHttpHostAvailability.py
User:               Guodong
Create Date:        2016/10/26
Create Time:        12:09

Function:
    test Http Host Availability

Some helpful message:
    For CentOS: yum -y install python-devel python-pip; pip install gevent
    For Ubuntu: apt-get -y install python-dev python-pip; pip install gevent
    For Windows: pip install gevent
 """
import signal
import time
import sys
#  execute some operations concurrently using python
from gevent import monkey

monkey.patch_all()
import gevent
import urllib2

hosts = ['https://webpush.wx2.qq.com/cgi-bin/mmwebwx-bin/synccheck',
         'https://webpush.wx.qq.com/cgi-bin/mmwebwx-bin/synccheck', ]

errorStopCounts = 200

quit_flag = False
statistics = dict()


def changeQuit_flag(signum, frame):
    del signum, frame
    global quit_flag
    quit_flag = True
    print "Canceled task on their own by the user."


def testNoHttpResponseException(url):
    tryFlag = True
    global quit_flag
    errorCounts = 0
    tryCounts = 0
    global statistics
    globalStartTime = time.time()
    while tryFlag:
        if not quit_flag:
            tryCounts += 1
            print('GET: %s' % url)
            try:
                startTime = time.time()
                resp = urllib2.urlopen(url)  # using module 'request' will be better, request will return header info..
                endTime = time.time()
                data = resp.read()
                responseTime = endTime - startTime
                print '%d bytes received from %s. response time is: %s' % (len(data), url, responseTime)
                print "data received from %s at %d try is: %s" % (url, tryCounts, data)
                gevent.sleep(2)
            except urllib2.HTTPError as e:
                errorCounts += 1
                statistics[url] = errorCounts
                currentTime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
                print "HTTPError occurred, %s, and this is %d times(total) occurs on %s at %s." % (
                    e, statistics[url], url, currentTime)

                if errorCounts >= errorStopCounts:
                    globalEndTime = time.time()
                    tryFlag = False
            except Exception as e:
                # Exception, such as 'error: [Errno 104] Connection reset by peer'
                print "Error occurred, %s on %s" % (e, url)
                time.sleep(2)
        else:
            globalEndTime = time.time()
            break

    for url in statistics:
        print "Total error counts is %d on %s" % (statistics[url], url)
        hosts.remove(url)
    for url in hosts:
        print "Total error counts is 0 on %s" % url
    globalUsedTime = globalEndTime - globalStartTime
    print "Total time use is %s" % globalUsedTime
    sys.exit(0)


try:
    # Even if the user cancelled the task,
    # it also can statistics the number of errors and the consumption of time for each host.
    signal.signal(signal.SIGINT, changeQuit_flag)

    gevent.joinall([gevent.spawn(testNoHttpResponseException, host) for host in hosts])
except KeyboardInterrupt:
    # Note: this line can NOT be reached, because signal has been captured!
    print "Canceled task on their own by the user."
    sys.exit(0)
