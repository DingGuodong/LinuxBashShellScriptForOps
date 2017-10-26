#!/usr/bin/python
# encoding: utf-8
# -*- coding: utf8 -*-
"""
Created by PyCharm.
File:               LinuxBashShellScriptForOps:emptyRecycleBin.py
User:               Guodong
Create Date:        2017/4/25
Create Time:        9:53
 """
import codecs
import locale

import winshell


def get_system_encoding():
    """
    The encoding of the default system locale but falls back to the given
    fallback encoding if the encoding is unsupported by python or could
    not be determined.  See tickets #10335 and #5846
    """
    try:
        encoding = locale.getdefaultlocale()[1] or 'ascii'
        codecs.lookup(encoding)
    except Exception as _:
        del _
        encoding = 'ascii'
    return encoding


DEFAULT_LOCALE_ENCODING = get_system_encoding()
try:
    winshell.recycle_bin().empty(confirm=False, show_progress=False, sound=False)
except Exception as e:
    print e, e.args[1].decode(DEFAULT_LOCALE_ENCODING)
