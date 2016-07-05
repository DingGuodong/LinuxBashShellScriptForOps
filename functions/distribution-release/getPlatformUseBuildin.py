#!/usr/bin/python
# encoding: utf-8
# -*- coding: utf8 -*-
import sys


def win_or_linux():
    if 'posix' in sys.builtin_module_names:
        os_type = 'Linux'
    elif 'nt' in sys.builtin_module_names:
        os_type = 'Windows'
    return os_type


def centos_or_ubuntu_or_debian():
    try:
        with open('/etc/issue', 'r') as f:
            linux_type = f.read().lower().strip().split(' ')[0]
    except IOError:
        pass
    else:
        if linux_type is not None:
            return linux_type

    try:
        with open('/etc/lsb-release', 'r') as f:
            linux_type = f.read().split('\n')[0].split('=')[1]
    except IOError:
        pass
    else:
        if linux_type is not None:
            return linux_type.lower()

    try:
        with open('/etc/os-release', 'r') as f:
            linux_type = f.read().split('\n')[0].split('=')[1]
    except IOError:
        pass
    else:
        if linux_type is not None:
            return linux_type.strip('"').lower()

    return "Unknown and unsupported system"


if __name__ == '__main__':
    print win_or_linux().lower()
    print centos_or_ubuntu_or_debian()
