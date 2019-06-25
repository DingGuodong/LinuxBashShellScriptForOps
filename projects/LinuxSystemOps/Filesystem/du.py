#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created by PyCharm.
File Name:              LinuxBashShellScriptForOps:get-all-directories-not-empty-and-no-subdir.py
Version:                0.0.1
Author:                 dgden
Author Email:           dgdenterprise@gmail.com
URL:                    https://github.com/DingGuodong/LinuxBashShellScriptForOps
Download URL:           https://github.com/DingGuodong/LinuxBashShellScriptForOps/tarball/master
Create Date:            2019/6/25
Create Time:            9:43
Description:            find directories larger than x bits
Long Description:       get all directories which not empty and have no subdir, then get total size order by size
References:             
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
import os
from sys import argv


def get_wanted_directories(path):
    path = os.path.abspath(path)
    for top, dirs, nondirs in os.walk(path):
        if not dirs and nondirs:
            yield top
        if len(nondirs) > 10:
            yield top


def get_size_of_directory(path):
    if os.path.isdir(path):
        size = 0
        for top, dirs, nondirs in os.walk(path):
            for filename in nondirs:
                full_path = os.path.join(top, filename)
                size += os.path.getsize(full_path)
        return size, path


def confirm(question, default=True):
    """
    Ask user a yes/no question and return their response as True or False.

    :parameter question:
    ``question`` should be a simple, grammatically complete question such as
    "Do you wish to continue?", and will have a string similar to " [Y/n] "
    appended automatically. This function will *not* append a question mark for
    you.
    The prompt string, if given,is printed without a trailing newline before reading.

    :parameter default:
    By default, when the user presses Enter without typing anything, "yes" is
    assumed. This can be changed by specifying ``default=False``.

    :return True or False
    """
    # Set up suffix
    if default:
        suffix = "Y/n"
    else:
        suffix = "y/N"
    # Loop till we get something we like
    while True:
        response = raw_input("%s [%s] " % (question, suffix)).lower()
        # Default
        if not response:
            return default
        # Yes
        if response in ['y', 'yes']:
            return True
        # No
        if response in ['n', 'no']:
            return False
        # Didn't get empty, yes or no, so complain and loop
        print("I didn't understand you. Please specify '(y)es' or '(n)o'.")


if __name__ == '__main__':
    if len(argv) == 2:
        given_path = argv[1]
        given_size = 100 * 1024 * 1024  # 100 MB
    elif len(argv) == 3:
        given_path = argv[1]
        given_size = int(argv[2])
    elif len(argv) == 1:
        given_path = '.'
        given_size = 100 * 1024 * 1024  # 100 MB
    else:
        raise RuntimeError("usage: %s [path] [size in bits]" % argv[0])

    wanted_path_list = []
    max_count_directories = 100000
    goon = False

    res = get_wanted_directories(given_path)
    for item in res:
        t_size, t_path = get_size_of_directory(item)
        if t_size > given_size:
            wanted_path_list.append((t_size, t_path))

        if len(wanted_path_list) > max_count_directories and not goon:
            user_answer = confirm("The given path has too many items(>%d) "
                                  "and more memory will be required, continue?") % max_count_directories
            if not user_answer:
                break
            else:
                goon = True

    for item in sorted(wanted_path_list, key=lambda x: x[0], reverse=True):
        print(item)
