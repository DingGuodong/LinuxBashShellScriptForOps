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
import codecs
import locale
import subprocess
import time
from threading import Timer


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


cmd = ["ping", "-t", "www.google.com"]
ping = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

my_timer = Timer(5, lambda process: process.kill(), [ping])
try:
    my_timer.start()
    print(time.ctime())
    stdout, stderr = ping.communicate()
    print(always_to_utf8(stdout), always_to_utf8(stderr))
finally:
    print(time.ctime())
    my_timer.cancel()
