#!/usr/bin/python
# encoding: utf-8
# -*- coding: utf8 -*-
"""
Created by PyCharm.
File Name:              LinuxBashShellScriptForOps:pyInitScriptRender.py
Version:                0.0.1
Author:                 Guodong
Author Email:           dgdenterprise@gmail.com
URL:                    https://github.com/DingGuodong/LinuxBashShellScriptForOps
Download URL:           https://github.com/DingGuodong/LinuxBashShellScriptForOps/tarball/master
Create Date:            2018/1/26
Create Time:            15:07
Description:            Renders a initscript template for CentOS and Ubuntu
Long Description:       Get distribution version
                        file can be used in Linux General Distribution:
                            /etc/issue
                            /proc/version
                        file can be used in Ubuntu:
                            /etc/lsb-release
                            /etc/os-release
                            /usr/lib/os-release
                        file can be used in CentOS:
                            /etc/system-release
                            /etc/redhat-release
                            /etc/centos-release
                            /etc/os-release (Systemd only, after 6)
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
import os

CENTOS_RELEASE_FILE = "/etc/centos-release"
UBUNTU_RELEASE_FILE = "/etc/issue"

UBUNTU_SYSTEMD_RELEASE_FILE = "/etc/os-release"
CENTOS_SYSTEMD_RELEASE_FILE = UBUNTU_SYSTEMD_RELEASE_FILE


def is_ubuntu():
    if os.path.exists(UBUNTU_RELEASE_FILE):
        with open(UBUNTU_RELEASE_FILE, "r") as f:
            if "ubuntu" in f.readline().lower():
                return True
            else:
                return False


def is_ubuntu14():
    # last non-systemd version
    version = get_version_id(centos=False, get_major=True)
    if version:
        if int(version) <= 14:
            return True
        else:
            return False
    return False


def is_centos():
    if os.path.exists(CENTOS_RELEASE_FILE):
        return True
    else:
        return False


def is_centos6():
    # last no-systemd version
    version = get_version_id(centos=True, get_major=True)
    if version:
        if int(version) <= 6:
            return True
        else:
            return False
    return False


def get_version_id(centos=True, get_major=False):
    if centos and is_centos():
        if os.path.exists(CENTOS_RELEASE_FILE):
            with open(CENTOS_RELEASE_FILE, "r") as f:
                if get_major:
                    return f.readline().strip().split()[2].split(".")[0]
                else:
                    return f.readline().strip().split()[2]
    if not centos and is_ubuntu():
        if os.path.exists(UBUNTU_RELEASE_FILE):
            with open(UBUNTU_RELEASE_FILE, "r") as f:
                if get_major:
                    return f.readline().strip().split()[1].split(".")[0]
                else:
                    return f.readline().strip().split()[1]
    return ""


if __name__ == '__main__':
    print("** usage example **")
    print("Ubuntu" if is_ubuntu() else "", end=' ')
    print("CentOS" if is_ubuntu() else "", end=' ')
    print(14 if is_ubuntu() and is_ubuntu14() else "", end=' ')
    print(16 if is_ubuntu() and not is_ubuntu14() else "", end=' ')
    print(6 if is_centos() and is_centos6() else "", end=' ')
    print(7 if is_centos() and not is_centos6() else "", end=' ')
