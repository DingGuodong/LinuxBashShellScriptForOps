#!/usr/bin/python
# encoding: utf-8
# -*- coding: utf8 -*-
"""
Created by PyCharm.
File:               LinuxBashShellScriptForOps:manage.py.py
User:               Guodong
Create Date:        2016/9/29
Create Time:        10:11
 """
from fabric.api import *
from fabric.colors import *
from fabric.context_managers import *
from fabric.contrib.console import confirm
from IPy import IP
import logging
import logging.handlers
import time
import os
import sys
import re

BASE = "nginx"


def usage():
    print("using this script install nginx for specified host or hosts group.")
    print("""Example:
    fab -i <PATH> -f <PATH> <command>

    -i <PATH>    path to SSH private key file. May be repeated.
    -f <PATH>    this file's full name, such as \'manage.py\'.
    <command>    def name in this file.
    """)
    sys.exit(1)


def advice():
    print()


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


host = ''
hosts_list = list()
while True:
    if len(hosts_list) == 0:
        print("Please input host's IP for deploy %s here. <Press Enter to end input>" % BASE)
    host = input()
    if host == "":
        break
    else:
        try:
            host = str(IP(host, ipversion=4))
            hosts_list.append(host)
        except ValueError as e:
            print("Please input a valid IP address.")
            # want_continue = raw_input("Continue? y/n <default is NO>:\n")
            # if want_continue in ['Yes', 'YES', 'yes', 'Y', 'y']:
            #     continue
            # else:
            #     break
            if confirm("Do you wish to continue add host? <default is NO>", default=False):
                continue
            else:
                break

if len(hosts_list) == 0:
    print("No hostname specified, see usage for more :")
    usage()

env.hosts = list(set(hosts_list))  # remove duplicated host with set()

env.user = 'root'


def initLoggerWithRotate():
    current_time = time.strftime("%Y%m%d%H")
    logpath = "/tmp"
    logfile = "log_fabfile_" + current_time + ".log"
    if not os.path.exists(logpath):
        os.makedirs(logpath)
    else:
        logfile = os.path.join(logpath, logfile)

    logger = logging.getLogger("fabric")
    log_formatter = logging.Formatter("%(asctime)s %(filename)s:%(lineno)d %(name)s %(levelname)s: %(message)s",
                                      "%Y-%m-%d %H:%M:%S")
    file_handler = logging.handlers.RotatingFileHandler(logfile, maxBytes=104857600, backupCount=5)
    file_handler.setFormatter(log_formatter)
    stream_handler = logging.StreamHandler(sys.stderr)
    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)
    logger.setLevel(logging.DEBUG)
    return logger


log = initLoggerWithRotate()


def show_uname():
    try:
        out = run("uname -a")
    except KeyboardInterrupt:
        log.warning("We catch 'Ctrl + C' pressed, task canceled!")
        sys.exit(1)
    if out.return_code == 0:
        log.info("task finished successfully on " + env.host + " .")
    else:
        log.error("task finished failed on " + env.host + " .")


def load_script():
    script_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "nginx-install-centos.sh")
    if os.path.exists(script_path):
        try:
            print("uploading script file to %s" % env.host)
            put(script_path, '/tmp/' + os.path.basename(script_path))
            print("run script file on %s" % env.host)
            run("bash %s" % ('/tmp/' + os.path.basename(script_path)))
        except Exception as e:
            log.error("task load_script failed! msg: %s" % str(e))
            abort("task load_script failed! msg: %s" % str(e))
    else:
        print("Can NOT find script file.")


def terminal_debug(defName):
    print("This method is used to test this script file if works well, do not using it for production")
    try:
        usage()
    except SystemExit:
        pass
    command = r"fab -i c:\Users\Guodong\.ssh\exportedkey201310171355\
                -f %s \
                %s" % (__file__, defName)
    os.system(command)
    sys.exit(0)


if __name__ == '__main__':
    if len(sys.argv) == 1 and is_windows():
        terminal_debug("load_script")

    sys.argv[0] = re.sub(r'(-script\.pyw|\.exe)?$', '', sys.argv[0])
    print(red("Please use 'fab -f %s'" % " ".join(str(x) for x in sys.argv[0:])))
    sys.exit(1)
