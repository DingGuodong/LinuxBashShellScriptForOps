#!/usr/bin/python
# encoding: utf-8
# -*- coding: utf8 -*-
"""
Created by PyCharm.
File:               LinuxBashShellScriptForOps:pyFabricBatchManager.py
User:               Guodong
Create Date:        2017/7/12
Create Time:        11:13
Description:        python batch manager with Fabric, run command you input on Linux Systems
 """
import os
import sys
import re

try:
    from fabric.api import *
except ImportError:
    try:
        command_to_execute = "pip install fabric"
        os.system(command_to_execute)
    except OSError:
        exit(1)
finally:
    from fabric.api import *
    from fabric.main import main
    from fabric.colors import *

env.interactive_mode = True
env.test_env = 'TestEnvironment'
env.prod_env = 'ProductionEnvironment'
env.all_env = 'all'
env.roledefs = {
    env.test_env: ['10.45.51.99',
                   '10.46.68.233',
                   '10.47.49.161',
                   '10.46.69.219',
                   ],
    env.prod_env: ["10.160.46.5",
                   "10.160.8.189",
                   "10.25.0.93",
                   "10.24.232.132",
                   "10.171.168.179",
                   "10.172.200.22",
                   "10.132.10.244",
                   "10.132.5.122",
                   "10.132.4.168",
                   "10.132.1.123",
                   "10.132.0.59",
                   "10.132.10.208",
                   "10.47.50.145",
                   "10.47.162.31",
                   ],
}

env.roledefs[env.all_env] = [host for role in env.roledefs.values() for host in role]

env.port = 22
env.user = 'root'
env.key_filename = r'C:\Users\Guodong\.ssh\ebt-linux-centos-ssh-root-key.pem'
env.skip_bad_hosts = True
env.remote_interrupt = True


def tail_remote_file():
    assert (env.remote_interrupt is True)
    run("tail -f /var/log/messages || tail -f /var/log/syslog")


def run_command(command):
    # http://docs.fabfile.org/en/1.13/usage/fab.html#per-task-arguments
    run('uname -n -r -m')  # show hostname, etc
    run(command)


def terminal_debug(defName):
    command = "fab -i {ssh_key_filename} -f {fab_file} -R {roles} -D {task}".format(ssh_key_filename=env.key_filename,
                                                                                    roles=env.test_env,
                                                                                    fab_file=__file__,
                                                                                    task=defName)
    print command
    os.system(command)


def is_windows():
    return True if 'nt' in sys.builtin_module_names else False


def is_linux():
    # Note: not validate on Mac OS X
    return True if 'posix' in sys.builtin_module_names else False


if __name__ == '__main__':
    if len(sys.argv) == 1 and is_windows():
        if env.interactive_mode:
            print """
We trust you have received the usual lecture from the local System
Administrator. It usually boils down to these three things:

    #1) Respect the privacy of others.
    #2) Think before you type.
    #3) With great power comes great responsibility.
"""
            command_to_run = raw_input("Input the command to run:")
            if command_to_run != "":
                terminal_debug('run_command:command="{command}"'.format(command=command_to_run))
            else:
                print "Bad Input, now exit, bye."
                exit(1)
        else:
            terminal_debug('run_command:command="uname -a"')
        sys.exit(0)

    sys.argv[0] = re.sub(r'(-script\.pyw|\.exe)?$', '', sys.argv[0])
    print red("Please use 'fab -f %s'" % " ".join(str(x) for x in sys.argv[0:]))
    sys.exit(1)
