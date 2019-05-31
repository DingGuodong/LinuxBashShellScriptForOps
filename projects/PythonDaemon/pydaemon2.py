#!/usr/bin/python
# encoding: utf-8
# -*- coding: utf8 -*-
"""
Created by PyCharm.
File:               LinuxBashShellScriptForOps:pydaemon2
User:               Guodong
Create Date:        2016/8/8
Create Time:        14:47
 """
import time
from daemon import runner  # from python-daemon python-lockfile packages
import sys


class App(object):
    def __init__(self):
        self.stdin_path = '/dev/null'
        self.stdout_path = '/dev/tty'
        self.stderr_path = '/dev/tty'
        self.pidfile_path = '/tmp/foo.pid'
        self.pidfile_timeout = 5

    def run(self):
        while True:
            print("Howdy!  Gig'em!  Whoop!")
            time.sleep(2)


if len(sys.argv) < 2:
    print("usage: %s start|stop|restart" % __file__)
elif sys.argv[1] == "status":
    raise NotImplementedError
else:
    pass

app = App()
daemon_runner = runner.DaemonRunner(app)
daemon_runner.do_action()
