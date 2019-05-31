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
import re
import subprocess
import sys


def always_to_utf8(text):
    import locale

    encoding = locale.getpreferredencoding()
    if isinstance(text, bytes):
        try:
            return text.decode(encoding)
        except UnicodeDecodeError:
            return text.decode("utf-8")

    else:
        return text  # do not need decode, return original object if type is not instance of string type
        # raise RuntimeError("expected type is str, but got {type} type".format(type=type(text)))


def get_rtt_avg_ms_win_zh(string):
    pattern = re.compile(r'平均 = (\d)ms')
    match = pattern.search(string)
    if match:
        return match.group(1)


def get_rtt_avg_ms_posix_en(string):
    pattern = re.compile(r'rtt min/avg/max/mdev = ([\d.]*)/([\d.]*)/([\d.]*)/([\d.]*) ms')
    match = pattern.search(string)
    if match:
        return match.group(2)


def show_network_latency(hostname, ping_count=4, show_detail=False):
    mswindows = (sys.platform == "win32")  # learning from 'subprocess' module
    linux = (sys.platform == "linux2")

    hostname = ip = hostname

    if mswindows:
        if show_detail:
            print("ping %s on Windows..." % ip)
        proc_obj = subprocess.Popen(r'ping -n %d %s' % (ping_count, hostname), shell=True, stdout=subprocess.PIPE,
                                    stderr=subprocess.STDOUT)
        result = always_to_utf8(proc_obj.stdout.read())
        if show_detail:
            print(result)
        print(get_rtt_avg_ms_win_zh(result))

    if linux:
        if show_detail:
            print("ping %s on Linux..." % ip)
        # result = subprocess.check_output(["ping", hostname, "-c", "1"])
        proc_obj = subprocess.Popen(r'ping -c %d %s' % (ping_count, hostname), shell=True, stdout=subprocess.PIPE,
                                    stderr=subprocess.STDOUT)
        # return_code = proc_obj.returncode
        result = always_to_utf8(proc_obj.stdout.read())
        if show_detail:
            print(result)
        print(get_rtt_avg_ms_posix_en(result))


if __name__ == '__main__':
    show_network_latency("192.168.88.11", ping_count=4, show_detail=True)
