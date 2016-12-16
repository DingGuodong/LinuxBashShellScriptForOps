#!/usr/bin/python
# encoding: utf-8
# -*- coding: utf8 -*-
"""
Created by PyCharm.
File:               LinuxBashShellScriptForOps:getReturnCode.py
User:               Guodong
Create Date:        2016/12/13
Create Time:        15:28
 """
import sys
import subprocess

import codecs
import locale


def get_system_encoding():
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

mswindows = (sys.platform == "win32")  # learning from 'subprocess' module
linux = (sys.platform == "linux2")

hostname = ip = "192.168.1.1"
ping_count = 4

if mswindows:
    print "ping %s on Windows..." % ip
    for i in xrange(ping_count):
        proc_obj = subprocess.Popen(r'ping -n %d %s' % (1, hostname), shell=True, stdout=subprocess.PIPE,
                                    stderr=subprocess.STDOUT)
        result = proc_obj.stdout.read().lower().decode(DEFAULT_LOCALE_ENCODING)
        if "ttl" in result:
            print "ping %s successfully!" % hostname
        else:
            print "ping %s failed!" % hostname

if linux:
    print "ping %s on Linux..." % ip
    for i in xrange(ping_count):
        # result = subprocess.check_output(["ping", hostname, "-c", "1"])
        proc_obj = subprocess.Popen(r'ping -c %d %s' % (1, hostname), shell=True, stdout=subprocess.PIPE,
                                    stderr=subprocess.STDOUT)
        return_code = proc_obj.returncode
        result = proc_obj.stdout.read().lower().decode(DEFAULT_LOCALE_ENCODING)
        if result is not None and "ttl" in result:
            print "ping %s successfully!" % hostname
        else:
            print "ping %s failed! return code is: %s" % (hostname, return_code if return_code is not None else 1)
