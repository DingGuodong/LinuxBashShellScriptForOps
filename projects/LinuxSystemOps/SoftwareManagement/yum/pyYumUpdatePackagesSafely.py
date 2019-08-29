#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
Created by PyCharm.
File:               LinuxBashShellScriptForOps:pyYumUpdatePackagesSafely.py
User:               Guodong
Create Date:        2017/8/14
Create Time:        14:59
Description:        we can NOT use 'yum update -y' to update all packages on production environment,
                    but we can enable or disable repos and packages we do not want to use.

References:         How to get exit code when using Python subprocess communicate method?
                    https://stackoverflow.com/questions/5631624/how-to-get-exit-code-when-using-python-subprocess-communicate-method
 """

import sys


def get_system_encoding():
    import codecs
    import locale
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


def run_command_on_linux(command):
    import subprocess
    linux = (sys.platform == "linux2")
    if not linux:
        print("Error: Linux platform is supported only!")
        sys.exit(1)

    proc_obj = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE,
                                stderr=subprocess.STDOUT)
    stdout, stderr = proc_obj.communicate()
    return_code = proc_obj.returncode
    if return_code == 0:
        return stdout
    else:
        print("command execute failed, return code is {return_code}".format(return_code=return_code))
        print(stdout, stderr)
        sys.exit(1)


if __name__ == '__main__':
    DEFAULT_LOCALE_ENCODING = get_system_encoding()
    command_get_packages_list = r"yum check-update | sed '1,3d' | awk '{print $1}'"
    command_get_unwanted_packages_list = r"yum check-update | sed '1,3d' | awk '{print $1}' | grep -E '(gitlab|docker)'"
    result_get_packages_list = set(run_command_on_linux(command_get_packages_list).split('\n'))
    result_get_unwanted_packages_list = set(run_command_on_linux(command_get_unwanted_packages_list).split(' '))
    packages_to_install_list = result_get_packages_list - result_get_unwanted_packages_list
    for package in packages_to_install_list:
        try:
            run_command_on_linux(r"yum update -y {package}".format(package=package))
        except SystemExit:
            print("update failed, maybe due to already updated")
