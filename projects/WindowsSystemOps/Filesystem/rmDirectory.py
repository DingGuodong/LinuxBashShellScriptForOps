#!/usr/bin/python
# encoding: utf-8
# -*- coding: utf8 -*-
"""
Created by PyCharm.
File:               LinuxBashShellScriptForOps:rmDirectory.py
User:               Guodong
Create Date:        2016/12/15
Create Time:        17:33
 """
import shutil
import os
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

path = "C:\Windows.old"
cmd = 'ICACLS ' + path + ' /grant Everyone:F'

if os.path.isdir(path):
    proc_obj = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE,
                                stderr=subprocess.STDOUT)
    result = proc_obj.stdout.read().lower().decode(DEFAULT_LOCALE_ENCODING)
    print result

if os.path.isdir(path):
    try:
        shutil.rmtree(path)
    except WindowsError as e:
        if e.message:
            print e.message.decode(DEFAULT_LOCALE_ENCODING)
        if e.args:
            print e.args
