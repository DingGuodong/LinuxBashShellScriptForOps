#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created by PyCharm.
File Name:              LinuxBashShellScriptForOps:git-clone-until-success.py
Version:                0.0.1
Author:                 dgden
Author Email:           dgdenterprise@gmail.com
URL:                    https://github.com/DingGuodong/LinuxBashShellScriptForOps
Download URL:           https://github.com/DingGuodong/LinuxBashShellScriptForOps/tarball/master
Create Date:            2020/1/31
Create Time:            21:24
Description:            git clone until it succeeds
Long Description:       
References:             [GitPython homepage]https://github.com/gitpython-developers/GitPython
                        [GitPython User Documentation](https://gitpython.readthedocs.io/en/stable/)
Prerequisites:          pip2.7 install GitPython
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
import time

import git


def git_clone(repository, directory=".", branch='master', max_retries=10):
    KEEP_RUNNING_FLAG = True
    DEFAULT_RETRIES = 10
    MAX_RETRIES = max_retries if max_retries > 0 else DEFAULT_RETRIES
    MAX_RETRY_TIMES = 0

    while KEEP_RUNNING_FLAG and MAX_RETRY_TIMES <= MAX_RETRIES:
        try:
            git.Repo.clone_from(url=repository, to_path=directory, branch=branch)
        except git.GitCommandError as e:
            print(e)
            time.sleep(2)
            MAX_RETRY_TIMES += 1
            continue
        KEEP_RUNNING_FLAG = False


if __name__ == '__main__':
    repo_url = "https://github.com/django/django.git"
    # `git clone --branch=master -v https://github.com/django/django.git D:\GitHub\django`
    git_clone(repo_url, r"D:\GitHub\django")
