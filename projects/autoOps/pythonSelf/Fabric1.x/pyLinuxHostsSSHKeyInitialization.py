#!/usr/bin/python
# encoding: utf-8
# -*- coding: utf8 -*-
"""
Created by PyCharm.
File:               LinuxBashShellScriptForOps:pyLinuxHostsSSHKeyInitialization.py
User:               Guodong
Create Date:        2017/3/9
Create Time:        23:05
 """
import logging
import logging.handlers
import os
import sys
import time

from fabric.api import *
from fabric.colors import red, green, yellow, blue
from fabric.context_managers import *
from fabric.contrib.console import confirm

env.roledefs = {
    'base': ['ubuntu@192.168.1.101:22', ],
    "bigData": ['ubuntu@192.168.100.122:22', 'ubuntu@192.168.100.123:22', 'ubuntu@192.168.100.124:22', ],
    "coreServices": ['ubuntu@192.168.100.127:22', 'ubuntu@192.168.100.128:22', 'ubuntu@192.168.100.129:22',
                     'ubuntu@192.168.100.130:22', ],
    "webAppFrontend": ['ubuntu@192.168.100.125:22', ],
    "webAppBackend": ['ubuntu@192.168.100.126:22', ],
    'all': ['192.168.1.101', '192.168.100.122', '192.168.100.123', '192.168.100.124', '192.168.100.125',
            '192.168.100.126', '192.168.100.127', '192.168.100.128', '192.168.100.129', '192.168.100.130', ],
    'db': ['ubuntu@192.168.100.127:22', ],
    'nginx': ['ubuntu@192.168.100.128:22', ],
}

env.hosts = ['192.168.1.101', '192.168.100.122', '192.168.100.123', '192.168.100.124', '192.168.100.125',
             '192.168.100.126', '192.168.100.127', '192.168.100.128', '192.168.100.129', '192.168.100.130', ]
env.port = '22'
env.user = "ubuntu"
env.password = "ubuntu"
env.sudo_user = "root"  # fixed setting, it must be 'root'
env.sudo_password = "ubuntu"
env.disable_known_hosts = True
env.warn_only = False
env.command_timeout = 15
env.connection_attempts = 2


def initLoggerWithRotate(logPath="/var/log", logName=None, singleLogFile=True):
    current_time = time.strftime("%Y%m%d%H")
    if logName is not None and not singleLogFile:
        logPath = os.path.join(logPath, logName)
        logFilename = logName + "_" + current_time + ".log"
    elif logName is not None and singleLogFile:
        logPath = os.path.join(logPath, logName)
        logFilename = logName + ".log"
    else:
        logName = "default"
        logFilename = logName + ".log"

    if not os.path.exists(logPath):
        os.makedirs(logPath)
        logFilename = os.path.join(logPath, logFilename)
    else:
        logFilename = os.path.join(logPath, logFilename)

    logger = logging.getLogger(logName)
    log_formatter = logging.Formatter("%(asctime)s %(filename)s:%(lineno)d %(name)s %(levelname)s: %(message)s",
                                      "%Y-%m-%d %H:%M:%S")
    file_handler = logging.handlers.RotatingFileHandler(logFilename, maxBytes=104857600, backupCount=5)
    file_handler.setFormatter(log_formatter)
    stream_handler = logging.StreamHandler(sys.stderr)
    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)
    logger.setLevel(logging.DEBUG)
    return logger


mswindows = (sys.platform == "win32")  # learning from 'subprocess' module
linux = (sys.platform == "linux2")


def _win_or_linux():
    # os.name ->(sames to) sys.builtin_module_names
    if 'posix' in sys.builtin_module_names:
        os_type = 'Linux'
    elif 'nt' in sys.builtin_module_names:
        os_type = 'Windows'
    return os_type


def is_windows():
    if "windows" in _win_or_linux().lower():
        return True
    else:
        return False


def is_linux():
    if "linux" in _win_or_linux().lower():
        return True
    else:
        return False


def is_debian_family():
    import platform
    # http://stackoverflow.com/questions/2988017/string-comparison-in-python-is-vs
    # http://stackoverflow.com/questions/1504717/why-does-comparing-strings-in-python-using-either-or-is-sometimes-produce
    if platform.system() == "Linux":
        distname = platform.linux_distribution()
        if "Ubuntu" in distname or "Debian" in distname:
            return True
        else:
            return False
    else:
        return False


def is_rhel_family():
    import platform
    if platform.system() == "Linux":
        distname = platform.linux_distribution()
        if "CentOS" in distname or "Debian" in distname:
            return True
        else:
            return False
    else:
        return False


# log_path = "/var/log" if os.path.exists("/var/log") or os.makedirs("/var/log") else "/var/log"
log_path = "/var/log"
log_name = "." + os.path.splitext(os.path.basename(__file__))[0]

log = initLoggerWithRotate(logPath="/var/log", logName=log_name, singleLogFile=True)
log.setLevel(logging.INFO)


def is_valid_ipv4(ip, version=4):
    from IPy import IP
    try:
        result = IP(ip, ipversion=version)
    except ValueError:
        return False
    if result is not None and result != "":
        return True


@roles('all')
def reset_ssh_public_host_key():
    """
    First job to run
    Reset ssh public host key after clone from one same virtual machine template
    Repeat do this will disable ssh connect between different hosts which ssh key has been registered!
    :return:
    """
    with settings(warn_only=False):
        out = sudo("test -f /etc/ssh/unique.lck && cat /etc/ssh/unique.lck", combine_stderr=False, warn_only=True)
        print yellow(
            "Repeat do this will disable ssh connect between different hosts which ssh key has been registered!")

        if "1" not in out:
            if confirm("Are you really want to reset ssh public key on this host? "):
                blue("Reconfigure openssh-server with dpkg")
                sudo("rm /etc/ssh/ssh_host_* && dpkg-reconfigure openssh-server && echo 1 >/etc/ssh/unique.lck")
            else:
                print green("Brilliant, user canceled this dangerous operation.")
        else:
            print blue("If you see a 'Warning' in red color here, do not panic, this is normal when first time to run.")
            print green("ssh public host key is ok.")


@roles('all')
def inject_admin_ssh_public_key():
    """
    Second job to run
    Inject Admin user's ssh key to each host
    :return:
    """
    with settings(warn_only=False):
        sudo('yes | ssh-keygen -N "" -f /root/.ssh/id_rsa')
        content_ssh_public_key = """ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQCawuOgQup3Qc1OILytyH+u3S9te85ctEKTvzPtRjHfnEEOjpRS6v6/PsuDHplHO1PAm8cKbEZmqR9tg4mWSweosBYW7blUUB4yWfBu6cHAnJOZ7ADNWHHJHAYi8QFZd4SLAAKbf9J12Xrkw2qZkdUyTBVbm+Y8Ay9bHqGX7KKLhjt0FIqQHRizcvncBFHXbCTJWsAduj2i7GQ5vJ507+MgFl2ZTKD2BGX5m0Jq9z3NTJD7fEb2J6RxC9PypYjayXyQBhgACxaBrPXRdYVXmy3f3zRQ4/OmJvkgoSodB7fYL8tcUZWSoXFa33vdPlVlBYx91uuA6onvOXDnryo3frN1
ssh-rsa AAAAB3NzaC1yc2EAAAABJQAAAIEAumQ2srRwd9slaeYTdr/dGd0H4NzJ3uQdBQABTe/nhJsUFWVG3titj7JiOYjCb54dmpHoi4rAYIElwrolQttZSCDKTVjamnzXfbV8HvJapLLLJTdKraSXhiUkdS4D004uleMpaqhmgNxCLu7onesCCWQzsNw9Hgpx5Hicpko6Xh0=
"""
        sudo("echo -e '%s' >/root/.ssh/authorized_keys" % content_ssh_public_key)


@roles('all')
def scan_host_ssh_public_key():
    """
    Third and last job to run
    scan all host's public key, then inject to /root/.ssh/authorized_keys
    :return:
    """
    with settings(warn_only=False):
        for host in env.hosts:
            if is_valid_ipv4(host):
                sudo(
                    r"""ssh-keyscan -t rsa %s |& awk -F '[ ]+' '!/^#/ {print $2" "$3}' >>/root/.ssh/authorized_keys"""
                    % host)


@roles('all')
def config_ssh_connection():
    reset_ssh_public_host_key()
    inject_admin_ssh_public_key()
    scan_host_ssh_public_key()


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
    import re

    if len(sys.argv) == 1:
        if is_windows():
            terminal_debug_win32("config_ssh_connection")
            sys.exit(0)
        if is_linux():
            terminal_debug_posix("config_ssh_connection")
            sys.exit(0)

    sys.argv[0] = re.sub(r'(-script\.pyw|\.exe)?$', '', sys.argv[0])
    print red("Please use 'fab -f %s'" % " ".join(str(x) for x in sys.argv[0:]))
    sys.exit(1)
