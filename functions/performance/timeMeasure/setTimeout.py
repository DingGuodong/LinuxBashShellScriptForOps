#!/usr/bin/python
# encoding: utf-8
# -*- coding: utf8 -*-
"""
Created by PyCharm.
File:               LinuxBashShellScriptForOps:setTimeout.py
User:               Guodong
Create Date:        2017/1/16
Create Time:        9:50
Linux only
 """
import timeout


@timeout.timeout(timeout=5)
def test_timeout(seconds):
    import time
    print "start"
    time.sleep(seconds)
    print "end"


def test_timeout_with_content_manager(seconds):
    import time
    with timeout.timeout(timeout=5):
        print "start"
        time.sleep(seconds)
        print "end"


if __name__ == '__main__':
    import sys

    if sys.platform == "win32":
        print "skipped"
    else:
        test_timeout(6)
