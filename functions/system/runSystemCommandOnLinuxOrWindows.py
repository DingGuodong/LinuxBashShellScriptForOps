#!/usr/bin/python
# encoding: utf-8
# -*- coding: utf8 -*-
"""
Created by PyCharm.
File:               LinuxBashShellScriptForOps:runSystemCommandOnLinuxOrWindows.py.py
User:               Guodong
Create Date:        2017/2/6
Create Time:        16:58

Task:
    Run 'netsh winsock reset' on Windows to configure Windows Sockets.
    Restores the Winsock Catalog to a clean state and uninstalls all Winsock Layered Service Providers.
    The reset command restores the Winsock Catalog to a clean state. After the command is run,
    all Winsock LSPs that were previously installed must be reinstalled.
    This command does not affect Winsock Name Space Provider entries.
 """
import codecs
import locale
import subprocess
import sys

mswindows = (sys.platform == "win32")  # learning from 'subprocess' module
linux = (sys.platform == "linux2")


def get_system_encoding():
    """
    The encoding of the default system locale but falls back to the given
    fallback encoding if the encoding is unsupported by python or could
    not be determined.  See tickets #10335 and #5846
    """
    try:
        encoding = locale.getdefaultlocale()[1] or 'ascii'
        codecs.lookup(encoding)
    except Exception as _:
        del _
        encoding = 'ascii'
    return encoding


DEFAULT_LOCALE_ENCODING = get_system_encoding()


def _runCommandOnWindows(executable):
    if not executable or not isinstance(executable, (str, unicode)):
        print "parameter error, str type is required, but got type \'parameter_type\'.".format(
            parameter_type=type(executable))
        sys.exit(1)
    if mswindows:
        print "Run local command \'{command}\' on Windows...".format(command=executable)

        proc_obj = subprocess.Popen(executable, shell=True, stdout=subprocess.PIPE,
                                    stderr=subprocess.STDOUT)
        result = proc_obj.stdout.read().lower().decode(DEFAULT_LOCALE_ENCODING)
        if result:
            print result

    else:
        print "Windows Supported Only. Aborted!"
        sys.exit(1)


def _runCommandOnLinux(executable):
    if not executable or not isinstance(executable, (str, unicode)):
        print "parameter error, str type is required, but got type \'parameter_type\'.".format(
            parameter_type=type(executable))
        sys.exit(1)
    if linux:
        print "Run local command \'{command}\' on Linux...".format(command=executable)

        proc_obj = subprocess.Popen(executable, shell=True, stdout=subprocess.PIPE,
                                    stderr=subprocess.STDOUT)
        stdout, stderr = proc_obj.communicate()
        return_code = proc_obj.returncode
        if return_code == 0:
            print "Run local command \'{command}\' successfully!".format(command=executable)
            print stdout
        else:
            print "Run local command \'{command}\' failed! " \
                  "return code is: {return_code}".format(command=executable,
                                                         return_code=return_code if return_code is not None else 1)
            print stdout, stderr
    else:
        print "Linux Supported Only. Aborted!"
        sys.exit(1)


if __name__ == "__main__":
    command = "netsh winsock reset"
    if mswindows:
        _runCommandOnWindows(command)
    else:
        _runCommandOnLinux(command)
