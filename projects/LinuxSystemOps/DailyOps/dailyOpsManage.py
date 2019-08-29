#!/usr/bin/env python3
# -*- coding:utf-8 -*-
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

# TODO(Friendly prompt): if you have lots hosts to do, give this variable a hosts list, like env.hosts = [host1, host2,]
env.hosts = list()
env.user = 'root'
# TODO(Friendly prompt): give a shell script file to execute
file_to_execute = ""
debug = True


def usage():
    print("using this script execute scripts or command for specified host or hosts group.")
    print("""Example:
    fab -i <PATH> -f <PATH> <command>

    -i <PATH>    path to SSH private key file. May be repeated.
    -f <PATH>    this file's full name, such as \'dailyOpsManage.py\'.
    <command>    def name in this file.
    workable command are: load_command load_script
    """)
    sys.exit(1)


def advice():
    print


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


def get_hosts_list():
    hosts_list = list()
    while True:
        if len(hosts_list) == 0:
            print(cyan("Please input host's IP (input 1 at least). <Press Enter again to end input>"))
        host = input()
        if host == "":
            break
        else:
            try:
                host = str(IP(host, ipversion=4))
                hosts_list.append(host)
            except ValueError:
                print(red("Please input a valid IP address."))
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
        print(red("No hostname specified, see usage for more:"))
        usage()

    return list(set(hosts_list))  # remove duplicated host with set()


if debug and is_windows():
    debug_lock_filename = ".debug_lock_file"
    if len(env.hosts) == 0 and os.path.exists(debug_lock_filename):
        env.hosts = get_hosts_list()
else:
    if len(env.hosts) == 0:
        env.hosts = get_hosts_list()


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
    if file_to_execute == "":
        abort("it can NOT load script, please write it into this file, set \"file_to_execute = /path/to/filename\"")
    script_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), file_to_execute)
    if os.path.exists(script_path):
        try:
            print("uploading script file to %s" % env.host)
            put(script_path, '/tmp/' + os.path.basename(script_path))
            print("run script file on %s" % env.host)
            run("bash %s" % ('/tmp/' + os.path.basename(script_path)))
        except Exception as err:
            log.error("task load_script failed! msg: %s" % err.message)
            abort("task load_script failed! msg: %s" % err.message)
    else:
        print(red("Can NOT find script file."))


def load_command():
    # TODO(Guodong Ding) if read command from def inside, it will be a trouble and boring.
    print("""If you want to execute a same command to a set of hosts, using:
    $ fab [options] -- [shell command]
such as:
    $ fab -H system1,system2,system3 --port=22 --user=root --password=xxx -- uname -a
    Note: -H, comma-separated list of hosts to operate on, no blank space
    use fab --help for help.
Refer: http://docs.fabfile.org/en/1.12/usage/fab.html#arbitrary-remote-shell-commands
    """)
    while True:
        command = input(cyan("Please input command you want to execute?\n"))
        if command != "":
            break
        else:
            if confirm("Do you wish to continue? <default is NO>", default=False):
                continue
            else:
                abort("User canceled, now exit.")

    run(command, warn_only=True)


def terminal_debug(defName):
    print(blue("This method is used to test this script file if works well, do not using it for production"))
    global debug_lock_filename
    debug_lock_filename = ".debug_lock_file"
    with open(debug_lock_filename, 'w') as f:
        f.write("")
        f.flush()
    try:
        usage()
    except SystemExit:
        pass
    command = "fab -i c:\/Users\Guodong\.ssh\exportedkey201310171355 -f {} \ {}".format(__file__, defName)
    try:
        os.system(command)
        print(green("Command execute successfully! Finished!"))
    except SystemExit:
        pass
    finally:
        if os.path.exists(debug_lock_filename):
            os.remove(debug_lock_filename)
    sys.exit(0)


if __name__ == '__main__':
    if len(sys.argv) == 1 and is_windows():
        def_to_load = 0
        print(blue("Please input what behaviour do you want to deal?\n"
                   "1.load command;\n"
                   "2.load script;\n"
                   "enter number \"1\" to choose load command, enter \"2\" to choose load script."))
        def_to_load = int(input())
        if def_to_load == 1:
            terminal_debug("load_command")
        elif def_to_load == 2:
            terminal_debug("load_script")
        else:
            abort("Bad choice.")

    sys.argv[0] = re.sub(r'(-script\.pyw|\.exe)?$', '', sys.argv[0])
    print(red("Please use 'fab -f %s'" % " ".join(str(x) for x in sys.argv[0:])))
    sys.exit(1)
