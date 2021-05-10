#!/usr/bin/python
# coding=utf-8
"""
Created by PyCharm.
File Name:              LinuxBashShellScriptForOps:update_git_repos_by_pull.py
Version:                0.0.1
Author:                 Guodong
Author Email:           dgdenterprise@gmail.com
URL:                    https://github.com/DingGuodong/LinuxBashShellScriptForOps
Download URL:           https://github.com/DingGuodong/LinuxBashShellScriptForOps/tarball/master
Create Date:            2018/11/7
Create Time:            14:01
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
Programming Language:   Python :: 2.6
Programming Language:   Python :: 2.7
Topic:                  Utilities
 """
import os
import subprocess
from multiprocessing import Pool


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


def git_pull(path):
    """
    https://en.wikipedia.org/wiki/Thread_safety
    https://en.wikipedia.org/wiki/Linearizability#Atomic
    :param path:
    :return:
    """
    os.chdir(path)
    # TODO(Guodong Ding) we want to combines multiple standard outputs into one standard output
    os.system(
        "git remote get-url origin")  # not thread safe, because of operation is not Atomic
    os.system("git pull")


def git_pull_u1(path):
    """
    u1: combines multiple standard outputs into one standard output with external function "run_command_u1"
    :param path:
    :return:
    """
    os.chdir(path)
    return_code, stdout_part1 = run_command_u1("git remote get-url origin")
    return_code, stdout_part2 = run_command_u1("git pull")
    print("".join((stdout_part1, stdout_part2)))


def git_fetch_all(path):
    os.chdir(path)
    os.system("git fetch --all")


def run_workload(path):
    git_pull_u1(path)


git_top_directory = r'D:\GitHub'
git_repos_list = [os.path.join(git_top_directory, x) for x in os.listdir(git_top_directory) if
                  os.path.isdir(os.path.join(git_top_directory, x))]

if __name__ == '__main__':
    pool = Pool(4)  # 4 CPU cores
    pool.map(run_workload, git_repos_list)
