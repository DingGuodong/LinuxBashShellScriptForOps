#!/usr/bin/python
# encoding: utf-8
# -*- coding: utf8 -*-
import re
from copy import deepcopy

try:
    linux_type_dict = dict()
    with open('/etc/os-release', 'r') as f:
        linux_type_list = f.read().strip().split('\n')
except IOError:
    pass
else:
    if linux_type_list is not None:
        linux_type_list_to_purge = deepcopy(linux_type_list)
        # linux_type_list_to_purge = linux_type_list[:]  # another implement, sames to deepcopy
        for member in linux_type_list_to_purge:
            if re.search('^#+.*', member) is not None:
                member_to_purge = member
                linux_type_list.remove(member_to_purge)
        for member in linux_type_list:
            sub_member = member.split('=')
            linux_type_dict[sub_member[0]] = sub_member[1].strip('"')
        print linux_type_dict
        print linux_type_dict['ID']
