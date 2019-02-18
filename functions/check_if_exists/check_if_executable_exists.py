#!/usr/bin/python
# encoding: utf-8
# -*- coding: utf8 -*-
"""
Created by PyCharm.
File:               LinuxBashShellScriptForOps:check_if_executable_exists.py
User:               Guodong
Create Date:        2016/8/18
Create Time:        17:35
 """
import os
import sys


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


def is_exe(path):
    return os.path.isfile(path) and os.access(path, os.X_OK)


def which(path):
    if isinstance(path, str):
        pass
    else:
        return None

    fpath, fname = os.path.split(path)
    if fpath:
        if is_exe(path):
            return path
    else:
        if is_windows():
            if not path.endswith(".exe"):
                command = path + ".exe"
            else:
                command = path
        else:
            command = path

        for part in os.environ["PATH"].split(os.pathsep):
            part = part.strip('"')
            exe_file = os.path.join(part, command)
            if is_exe(exe_file):
                return exe_file

    return ""


if __name__ == '__main__':
    print(which("ping.exe"))
    print(which("ping"))
