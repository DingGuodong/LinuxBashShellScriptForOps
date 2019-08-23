#!/usr/bin/python
# encoding: utf-8
# -*- coding: utf8 -*-
"""
Created by PyCharm.
File Name:              LinuxBashShellScriptForOps:pyPythonicRunSystemCommand.py
Version:                0.0.1
Author:                 Guodong
Author Email:           dgdenterprise@gmail.com
URL:                    https://github.com/DingGuodong/LinuxBashShellScriptForOps
Download URL:           https://github.com/DingGuodong/LinuxBashShellScriptForOps/tarball/master
Create Date:            2018/1/24
Create Time:            15:43
Description:            simple and pythonic system command executor
Long Description:       
References:             https://github.com/ajenti/ajenti/blob/1.x/ajenti/api/helpers.py
Prerequisites:          []
Development Status:     3 - Alpha, 5 - Production/Stable
Environment:            Console
Intended Audience:      System Administrators, Developers, End Users/Desktop
License:                Freeware, Freely Distributable
Natural Language:       English, Chinese (Simplified)
Operating System:       POSIX :: Linux, Microsoft :: Windows
Programming Language:   Python :: 2.6
Programming Language:   Python :: 2.7
Topic:                  Utilities
 """
import subprocess
import sys

import gevent


def run_command(executable):
    """
    run system command by subprocess.Popen in silent
    :param executable: executable command
    :return: return_code, stdout, stderr
    """
    proc_obj = subprocess.Popen(executable, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = proc_obj.communicate()
    return_code = proc_obj.returncode
    return return_code, stdout, stderr


def run_command_u1(executable):
    """
    run system command by subprocess.
    u1: Combine stdout and stderr into stdout, such as 'exec >file 2>&1'
    :param executable: executable command
    :return: return_code, stdout, stderr
    """
    proc_obj = subprocess.Popen(executable, shell=True, stdout=subprocess.PIPE,
                                stderr=subprocess.STDOUT)  # Combine stdout and stderr into stdout
    stdout, stderr = proc_obj.communicate()
    return_code = proc_obj.returncode
    return return_code, stdout


def run(command):
    """
    run system command as if it were executed directly from the command line
    :param command:
    :return: return_code
    """
    return subprocess.call(command, shell=True)  # same as "os.system()"


def run_check_output(command):
    """
    not very well, see to 'KNOWN ISSUE'
    :param command:
    :return:
    """
    p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
    while True:
        out = p.stdout.read(1)
        if out == '' and p.poll() is not None:
            break
        if out != '':
            """
            KNOWN ISSUE: UnicodeDecodeError in Microsoft Windows
            """
            sys.stdout.write(out)
            sys.stdout.flush()


def subprocess_call_background(*args, **kwargs):
    p = subprocess.Popen(*args, **kwargs)
    gevent.sleep(0)
    return p.wait()


def subprocess_check_output_background(*args, **kwargs):
    p = subprocess.Popen(*args, stdout=subprocess.PIPE, **kwargs)
    gevent.sleep(0)
    return p.communicate()[0]


if __name__ == '__main__':
    # simple usage example
    subprocess_call_background(["/etc/init.d/nginx", "start"])

    for line in subprocess_check_output_background(['chkconfig', '--list']).splitlines():
        print line

    for line in subprocess_check_output_background(['service', '--status-all']).splitlines():
        print line

    subprocess_call_background(["ls", "-al"])

    for line in subprocess_check_output_background(['ls', '-al']).splitlines():
        print line
