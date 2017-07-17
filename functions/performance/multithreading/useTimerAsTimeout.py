#!/usr/bin/python
# encoding: utf-8
# -*- coding: utf8 -*-
"""
Created by PyCharm.
File:               LinuxBashShellScriptForOps:useTimerAsTimeout.py
User:               Guodong
Create Date:        2017/7/17
Create Time:        16:31
Description:        use Timer from threading module as timeout content manager
References:         
 """
import subprocess
from threading import Timer
import time
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

cmd = ["ping", "-t", "www.google.com"]
ping = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

my_timer = Timer(5, lambda process: process.kill(), [ping])
try:
    my_timer.start()
    print time.ctime()
    stdout, stderr = ping.communicate()
    print stdout.decode(DEFAULT_LOCALE_ENCODING), stderr.decode(DEFAULT_LOCALE_ENCODING)
finally:
    print time.ctime()
    my_timer.cancel()
