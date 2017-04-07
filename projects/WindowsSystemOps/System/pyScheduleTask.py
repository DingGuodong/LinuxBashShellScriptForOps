#!/usr/bin/python
# encoding: utf-8
# -*- coding: utf8 -*-
"""
Created by PyCharm.
File:               LinuxBashShellScriptForOps:pyScheduleTask.py
User:               Guodong
Create Date:        2017/4/6
Create Time:        22:33
 """
# https://docs.python.org/2/library/sched.html
import threading
import sched
import time
import sys
import locale
import codecs


def get_system_encoding():
    """
    The encoding of the default system locale but falls back to the given
    fallback encoding if the encoding is unsupported by python or could
    not be determined.  See tickets #10335 and #5846
    """
    try:
        encoding = locale.getdefaultlocale()[1] or 'ascii'
        codecs.lookup(encoding)
    except LookupError:
        encoding = 'ascii'
    return encoding


DEFAULT_LOCALE_ENCODING = get_system_encoding()


def shutdown_NetEaseCloudMusic(name):
    # define NetEaseCloudMusic process name
    ProcessNameToKill = name

    print
    import psutil
    import sys

    # learn from getpass.getuser()
    def getuser():
        """Get the username from the environment or password database.

        First try various environment variables, then the password
        database.  This works on Windows as long as USERNAME is set.

        """

        import os

        for username in ('LOGNAME', 'USER', 'LNAME', 'USERNAME'):
            user = os.environ.get(username)
            if user:
                return user

    currentUserName = getuser()

    if ProcessNameToKill in [x.name() for x in psutil.process_iter()]:
        print "[I] Process \"%s\" is found!" % ProcessNameToKill
    else:
        print "[E] Process \"%s\" is NOT running!" % ProcessNameToKill
        sys.exit(1)

    for process in psutil.process_iter():
        if process.name() == ProcessNameToKill:
            try:
                # root user can only kill its process, but can NOT kill other users process
                if process.username().endswith(currentUserName):
                    process.kill()
                    print "[I] Process \"%s(pid=%s)\" is killed successfully!" % (process.name(), process.pid)
            except Exception as e:
                print e


def display_countdown(sec):
    def countdown(secs):
        """
        blocking process 1
        :param secs: seconds, int
        :return:
        """
        current_time = time.strftime("%Y-%m-%d %H:%M:%S %Z").decode(DEFAULT_LOCALE_ENCODING).encode("utf-8")
        print "Time current: %s" % current_time
        while secs:
            now = time.strftime("%Y-%m-%d %H:%M:%S %Z").decode(DEFAULT_LOCALE_ENCODING).encode("utf-8")
            hours, seconds = divmod(secs, 3600)
            minutes, seconds = divmod(seconds, 60)
            clock_format = '{:02d}:{:02d}:{:02d}'.format(hours, minutes, seconds)
            sys.stdout.write('\rTime now: %s Time left: %s' % (now, clock_format))
            sys.stdout.flush()
            time.sleep(1)
            secs -= 1

    # set a human readable timer here, such as display how much time left to shutdown
    countdown(int(sec))


def display_scheduler(name):
    """
    blocking process 2
    :return:
    """
    s = sched.scheduler(time.time, time.sleep)
    s.enter(10, 1, shutdown_NetEaseCloudMusic, (name,))
    s.run()
    now = time.strftime("%Y-%m-%d %H:%M:%S %Z").decode(DEFAULT_LOCALE_ENCODING).encode("utf-8")
    print "Time finished: %s\nGood bye!" % now


if __name__ == '__main__':
    seconds_to_shutdown = 10
    process_name_to_shutdown = "cloudmusic.exe"

    threadingPool = list()
    threading_1 = threading.Thread(target=display_countdown, args=(seconds_to_shutdown,))
    threading_2 = threading.Thread(target=display_scheduler, args=(process_name_to_shutdown,))
    threadingPool.append(threading_1)
    threadingPool.append(threading_2)

    for thread in threadingPool:
        thread.setDaemon(False)
        thread.start()

    thread.join()
