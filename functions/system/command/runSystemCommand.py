#!/usr/bin/python
# encoding: utf-8
# -*- coding: utf8 -*-
"""
Created by PyCharm.
File:               LinuxBashShellScriptForOps:getReturnCode.py
User:               Guodong
Create Date:        2016/12/13
Create Time:        15:28
 """


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


def run(command):
    import subprocess

    p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE,
                         stderr=subprocess.STDOUT)
    (stdout, stderr) = p.communicate()

    if p.returncode != 0:
        print("encountered an error (return code %s) while executing '%s'" % (p.returncode, command))
        if stdout is not None:
            print("Standard output:", always_to_utf8(stdout))
        if stderr is not None:
            print("Standard error:", always_to_utf8(stderr))

        return False
    else:
        if stdout is not None:
            print(always_to_utf8(stdout))
        return True


if __name__ == '__main__':
    import os

    home = os.path.expanduser('~')  # both Windows and Linux is works. see also, os.devnull
    run('ls {linux_home} || dir {windows_home}'.format(linux_home=home, windows_home=home))
