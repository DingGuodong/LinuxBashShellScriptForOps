#!/usr/bin/python
# encoding: utf-8
# -*- coding: utf8 -*-
"""
Created by PyCharm.
File:               LinuxBashShellScriptForOps:killProcessByName.py
User:               Guodong
Create Date:        2016/10/31
Create Time:        16:56
 """
import psutil


# learn from getpass.getuser()
def getuser():
    """Get the username from the environment or password database.

    First try various environment variables, then the password
    database.  This works on Windows as long as USERNAME is set.

    """

    import os

    for name in ('LOGNAME', 'USER', 'LNAME', 'USERNAME'):
        user = os.environ.get(name)
        if user:
            return user


currentUserName = getuser()
ProcessNameToKill = 'chrome.exe'

if ProcessNameToKill in [x.name() for x in psutil.process_iter()]:
    print("Process \"%s\" is found!" % ProcessNameToKill)
else:
    print("Process \"%s\" is NOT running!" % ProcessNameToKill)

for process in psutil.process_iter():
    if process.name() == ProcessNameToKill:
        try:
            # root user can only kill its process, but can NOT kill other users process
            if process.username().endswith(currentUserName):
                process.kill()
                print("Process \"%s(pid=%s)\" is killed!" % (process.name(), process.pid))
        except Exception as e:
            print(e)
