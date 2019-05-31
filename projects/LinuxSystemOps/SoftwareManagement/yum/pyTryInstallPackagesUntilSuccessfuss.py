#!/usr/bin/python
# encoding: utf-8
# -*- coding: utf8 -*-
"""
Created by PyCharm.
File Name:              LinuxBashShellScriptForOps:pyTryInstallPackagesUntilSuccessfuss.py
Version:                0.0.1
Author:                 Guodong
Author Email:           dgdenterprise@gmail.com
URL:                    https://github.com/DingGuodong/LinuxBashShellScriptForOps
Download URL:           https://github.com/DingGuodong/LinuxBashShellScriptForOps/tarball/master
Create Date:            2017/12/7
Create Time:            17:18
Description:            
Long Description:       
References:             
Prerequisites:          []
Development Status:     3 - Alpha, 5 - Production/Stable
Environment:            Console
Intended Audience:      System Administrators, Developers, End Users/Desktop
License:                Freeware, Freely Distributable
Natural Language:       English, Chinese (Simplified)
Operating System:       POSIX :: Linux, Microsoft :: Windows
Programming Language:   Python :: 3

Topic:                  Utilities
 """
import time


def always_to_utf8(text):
    import locale

    encoding = locale.getpreferredencoding()
    if isinstance(text, bytes):
        try:
            return text.decode(encoding)
        except UnicodeDecodeError:
            return text.decode("utf-8")

    else:
        return text  # do not need decode, return original object if type is not instance of string type
        # raise RuntimeError("expected type is str, but got {type} type".format(type=type(text)))


def fn_timer(func):
    from functools import wraps

    @wraps(func)
    def function_timer(*args, **kwargs):
        import time
        time_begin = time.time()
        result = func(*args, **kwargs)
        time_end = time.time()
        print("Total time running {function_name}: {time_spent} seconds".format(function_name=func.__name__,
                                                                                time_spent=(time_end - time_begin)))

        return result

    return function_timer


@fn_timer
def run(command, capture_stdout=False, suppress_stdout=False):
    import subprocess

    p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE,
                         stderr=subprocess.STDOUT)
    (stdout, stderr) = p.communicate()

    if p.returncode != 0:  # run command failed
        print("encountered an error (return code %s) while executing '%s'" % (p.returncode, command))
        if stdout is not None:
            print("Standard output:\n", always_to_utf8(stdout))
        if stderr is not None:
            print("Standard error:\n", always_to_utf8(stderr))
        if not capture_stdout:
            return False
        else:
            return ""
    else:  # run command success

        if stdout is not None:
            if capture_stdout:
                return stdout
            else:
                if not suppress_stdout:
                    print(always_to_utf8(stdout))
                return True


if __name__ == '__main__':
    run("uname -a")
    keep_running_flay = True

    while keep_running_flay:
        print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))

        if run("yum install -y mongodb-org"):
            print("Successfully")
            keep_running_flay = False
        else:
            print("Failed")
            time.sleep(2)
