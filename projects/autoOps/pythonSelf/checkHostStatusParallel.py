#!/usr/bin/python
# encoding: utf-8
# -*- coding: utf8 -*-
from fabric.api import *
from fabric.colors import *
from fabric.context_managers import *
import os
import sys
import re

env.roledefs = {
    'test': ['root@10.6.28.28:22', ],
    'nginx': ['root@10.6.28.46:22', 'root@10.6.28.27:22', ],
    'db': ['root@10.6.28.35:22', 'root@10.6.28.93:22', ],
    'sit': ['root@10.6.28.46:22', 'root@10.6.28.135:22', 'root@10.6.28.35:22', ],
    'uat': ['root@10.6.28.27:22', 'root@10.6.28.125:22', 'root@10.6.28.93:22', ],
    'all': ["10.6.28.27", "10.6.28.28", "10.6.28.35", "10.6.28.46", "10.6.28.93", "10.6.28.125", "10.6.28.135"]
}

env.user = "root"
env.hosts = ["10.6.28.27", "10.6.28.28", "10.6.28.35", "10.6.28.46", "10.6.28.93", "10.6.28.125", "10.6.28.135"]
env.command_timeout = 15
env.connection_attempts = 2


def win_or_linux():
    # os.name ->(sames to) sys.builtin_module_names
    if 'posix' in sys.builtin_module_names:
        os_type = 'Linux'
    elif 'nt' in sys.builtin_module_names:
        os_type = 'Windows'
    return os_type


def is_windows():
    if "windows" in win_or_linux().lower():
        return True
    else:
        return False


def is_linux():
    if "linux" in win_or_linux().lower():
        return True
    else:
        return False


# ################################################################
# @parallel is not supported on Windows System
def showUptime():
    run("uptime")


def showVmstat():
    run("vmstat -w", warn_only=True)


def showMemory():
    run("free -m")


def showDiskUsage():
    run("df -h")


# ################################################################


def terminal_debug_win32(func):
    command = "fab -i c:\Users\Guodong\.ssh\exportedkey201310171355\
                -f %s \
                %s" % (__file__, func)
    os.system(command)


def terminal_debug_posix(func):
    command = "fab -i /etc/ssh/ssh_host_rsa_key\
                -f %s \
                %s" % (__file__, func)
    os.system(command)


if __name__ == '__main__':
    if len(sys.argv) == 1:
        if is_windows():
            terminal_debug_win32("showUptime showVmstat showMemory showDiskUsage")
            sys.exit(0)
        if is_linux():
            terminal_debug_posix("showUptime showVmstat showMemory showDiskUsage")
            sys.exit(0)

    sys.argv[0] = re.sub(r'(-script\.pyw|\.exe)?$', '', sys.argv[0])
    print red("Please use 'fab -f %s'" % " ".join(str(x) for x in sys.argv[0:]))
    sys.exit(1)
