#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created by PyCharm.
File Name:              LinuxBashShellScriptForOps:git-pull-with-gitpython.py
Version:                0.0.1
Author:                 dgden
Author Email:           dgdenterprise@gmail.com
URL:                    https://github.com/DingGuodong/LinuxBashShellScriptForOps
Download URL:           https://github.com/DingGuodong/LinuxBashShellScriptForOps/tarball/master
Create Date:            2019/11/1
Create Time:            14:20
Description:            update git repository with GitPython
Long Description:       
References:             
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

import os
from multiprocessing import Pool

import git

git_top_dir = r"D:\GitHub"
os.chdir(git_top_dir)

repos_dir = [os.path.join(git_top_dir, x) for x in os.listdir(git_top_dir)]


def git_pull(path):
    print("current repo path: %s" % path)
    repo = git.Repo(path)

    repo_info = repo.config_reader()
    print(repo_info.get_value('remote "origin"', "url"))

    if repo.bare:
        return True
    elif not repo.is_dirty():
        remote = repo.remote()
        try:
            remote.pull()
        except Exception as e:
            print(e)
            pass


if __name__ == '__main__':
    pool = Pool(2)
    pool.map(git_pull, repos_dir)
