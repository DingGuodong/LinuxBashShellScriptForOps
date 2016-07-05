#!/usr/bin/python
# encoding: utf-8
# -*- coding: utf8 -*-
import os
import sys
import re

try:
    import platform
except ImportError:
    pass
else:
    print platform.uname()
    print platform.linux_distribution()
    print platform.system()
# TODO(Guodong Ding) , continue here

print os.name
print sys.platform

if 'nt' in os.name:
    print 'Windows'
elif 'posix' in os.name:
    print 'Linux'

try:
    with open('/etc/issue') as f:
        content = f.read().lower().strip()
        output_list = re.split(r' ', content)
        linux_type = list(output_list)[0]
except IOError:
    pass
else:
    if linux_type is not None:
        print linux_type
