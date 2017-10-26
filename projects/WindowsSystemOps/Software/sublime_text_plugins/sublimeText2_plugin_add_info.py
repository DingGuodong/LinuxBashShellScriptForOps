#!/usr/bin/python
# encoding: utf-8
# -*- coding: utf8 -*-
"""
Created by PyCharm.
File:               LinuxBashShellScriptForOps:sublimeText2_plugin_add_info.py
User:               Guodong
Create Date:        2017/1/13
Create Time:        11:22

C:\Users\Guodong\AppData\Roaming\Sublime Text 2\Packages\User
https://code.tutsplus.com/tutorials/how-to-create-a-sublime-text-2-plugin--net-22685
Open the Sublime console by pressing ctrl+`. This is a Python console that has access to theAPI.

 """
import os
import time

import sublime_plugin


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
            except Exception as _:
                del _
                encoding = 'ascii'
            return encoding

        DEFAULT_LOCALE_ENCODING = get_system_encoding()
        raw_now = time.strftime('%a %b %d %H:%M:%S %Z %Y', time.localtime(time.time()))
        now = raw_now.decode(DEFAULT_LOCALE_ENCODING)
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
