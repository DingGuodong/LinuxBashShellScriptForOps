#!/usr/bin/python
# encoding: utf-8
# -*- coding: utf8 -*-
"""
Created by PyCharm.
File:               LinuxBashShellScriptForOps:network_latency.py
User:               Guodong
Create Date:        2017/7/26
Create Time:        17:36
Description:        show average network latency on Windows or Linux, return value(not int type in Linux)
References:         
 """
import sys
import subprocess
import re


def get_rtt_avg_ms_win_zh(string):
    pattern = re.compile(u'平均 = (\d)ms')
    match = pattern.search(string)
    if match:
        return match.group(1)


def get_rtt_avg_ms_posix_en(string):
    pattern = re.compile('rtt min/avg/max/mdev = ([\d.]*)/([\d.]*)/([\d.]*)/([\d.]*) ms')
    match = pattern.search(string)
    if match:
        return match.group(2)


def show_network_latency(hostname, ping_count=4, show_detail=False):
    mswindows = (sys.platform == "win32")  # learning from 'subprocess' module
    linux = (sys.platform == "linux2")

    hostname = ip = hostname

    if mswindows:
        def get_system_encoding():
            import codecs
            import locale
            """
            The encoding of the default system locale but falls back to the given
            fallback encoding if the encoding is unsupported by python or could
            not be determined.  See tickets #10335 and #5846
            """
            try:
                encoding = locale.getdefaultlocale()[1] or 'ascii'
                codecs.lookup(encoding)
            except Exception:
                encoding = 'ascii'
            return encoding

        DEFAULT_LOCALE_ENCODING = get_system_encoding()
        if show_detail:
            print "ping %s on Windows..." % ip
        proc_obj = subprocess.Popen(r'ping -n %d %s' % (ping_count, hostname), shell=True, stdout=subprocess.PIPE,
                                    stderr=subprocess.STDOUT)
        result = proc_obj.stdout.read().lower().decode(DEFAULT_LOCALE_ENCODING)
        if show_detail:
            print result
        print get_rtt_avg_ms_win_zh(result)

    if linux:
        if show_detail:
            print "ping %s on Linux..." % ip
        # result = subprocess.check_output(["ping", hostname, "-c", "1"])
        proc_obj = subprocess.Popen(r'ping -c %d %s' % (ping_count, hostname), shell=True, stdout=subprocess.PIPE,
                                    stderr=subprocess.STDOUT)
        # return_code = proc_obj.returncode
        result = proc_obj.stdout.read().lower().decode(DEFAULT_LOCALE_ENCODING)
        if show_detail:
            print result
        print get_rtt_avg_ms_posix_en(result)


if __name__ == '__main__':
    show_network_latency("192.168.88.11", ping_count=4, show_detail=False)
