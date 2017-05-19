#!/usr/bin/python3
# encoding: utf-8
# -*- coding: utf8 -*-
"""
Created by PyCharm.
File:               LinuxBashShellScriptForOps:sublimeText3_plugin_add_info.py
User:               Guodong
Create Date:        2017/5/18
Create Time:        09:12

Open the Sublime console by pressing ctrl+`. This is a Python console that has access to theAPI.
http://www.cnblogs.com/geekard/archive/2012/10/04/python-string-endec.html

 """
import sublime_plugin
import time
import os


class add_info(sublime_plugin.TextCommand):
    def run(self, edit):
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

        raw_now = time.strftime('%a %b %d %H:%M:%S %Y', time.localtime(time.time()))
        # TODO(Guodong Ding)
        # in SublimeText3, %z in time,strftime() can NOT decoding well, we need a good plan.
        # Python 3 different
        # DEFAULT_LOCALE_ENCODING = get_system_encoding()
        # now = raw_now.encode(DEFAULT_LOCALE_ENCODING, 'ignore').decode(DEFAULT_LOCALE_ENCODING)
        now = raw_now
        author = "default"

        for name in ('LOGNAME', 'USER', 'LNAME', 'USERNAME'):
            user = os.environ.get(name)
            if user:
                author = user
                break
        contents = {
            "contents": """
#
# @Author:      %s
# @DateTime:    %s
# @Description: Description
#
""" % (author, now)
        }
        self.view.run_command("insert_snippet", contents)
