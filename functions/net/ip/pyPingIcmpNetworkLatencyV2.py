#!/usr/bin/python
# encoding: utf-8
# -*- coding: utf8 -*-
"""
Created by PyCharm.
File:               LinuxBashShellScriptForOps:pyPingIcmpNetworkLatencyV2.py
User:               Guodong
Create Date:        2016/12/1
Create Time:        10:15
 """
import os
import sys
import subprocess

hostname = ip = "192.168.1.1"
count = 4


def win_or_linux():
    # os.name ->(sames to) sys.builtin_module_names
    if 'posix' in sys.builtin_module_names:
        os_type = 'Linux'
    elif 'nt' in sys.builtin_module_names:
        os_type = 'Windows'
    return os_type


def is_windows():
    if "windows" in win_or_linux().lower():
        return True
    else:
        return False


def is_linux():
    if "linux" in win_or_linux().lower():
        return True
    else:
        return False


mswindows = (sys.platform == "win32")  # learning from 'subprocess' module
# linux = (sys.platform == "linux2")

if is_windows() or mswindows:
    print "ping %s on Windows..." % ip
    for i in xrange(count):
        message = subprocess.Popen(r'ping -n %d %s' % (1, hostname), shell=True, stdout=subprocess.PIPE,
                                   stderr=subprocess.STDOUT)
        result = message.stdout.read().lower()
        if "ttl" in result:
            print "ping %s successfully!" % hostname
        else:
            print "ping %s failed!" % hostname

if is_linux():
    print "ping %s on Linux..." % ip
    for i in xrange(count):
        # result = subprocess.check_output(["ping", hostname, "-c", "1"])
        message = subprocess.Popen(r'ping -c %d %s' % (1, hostname), shell=True, stdout=subprocess.PIPE,
                                   stderr=subprocess.STDOUT)
        result = message.stdout.read().lower()
        if "ttl" in result:
            print "ping %s successfully!" % hostname
        else:
            print "ping %s failed!" % hostname
