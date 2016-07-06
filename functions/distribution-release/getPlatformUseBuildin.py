#!/usr/bin/python
# encoding: utf-8
# -*- coding: utf8 -*-
import sys


def win_or_linux():
    # os.name ->(sames to) sys.builtin_module_names
    if 'posix' in sys.builtin_module_names:
        os_type = 'Linux'
    elif 'nt' in sys.builtin_module_names:
        os_type = 'Windows'
    return os_type


def centos_or_ubuntu():
    try:
        # for CentOS or Ubuntu
        with open('/etc/issue', 'r') as f:
            linux_type = f.read().lower().strip().split(' ')[0]
    except IOError:
        pass
    else:
        if linux_type is not None:
            return linux_type

    try:
        linux_type_dict = dict()
        with open('/etc/os-release', 'r') as f:
            linux_type_list = f.read().strip().split('\n')
    except IOError:
        pass
    else:
        if linux_type_list is not None:
            for member in linux_type_list:
                sub_member = member.split('=')
                linux_type_dict[sub_member[0]] = sub_member[1].strip('"')
            return linux_type_dict['ID']

    try:
        # for Ubuntu
        with open('/etc/lsb-release', 'r') as f:
            linux_type = f.read().split('\n')[0].split('=')[1]
    except IOError:
        pass
    else:
        if linux_type is not None:
            return linux_type.lower()

    try:
        # for CentOS
        with open('/etc/system-release', 'r') as f:
            linux_type = f.read().lower().strip().split(' ')[0]
    except IOError:
        pass
    else:
        if linux_type is not None:
            return linux_type

    return "Unknown and unsupported system"


def yum_or_dpkg():
    distro_type = centos_or_ubuntu()
    if 'centos' in distro_type or 'redhat' in distro_type or 'rhel' in distro_type:
        return 'yum'
    elif 'ubuntu' in distro_type or 'debian' in distro_type:
        return 'dpkg'


if __name__ == '__main__':
    print win_or_linux().lower()
    print centos_or_ubuntu()
    print yum_or_dpkg()
