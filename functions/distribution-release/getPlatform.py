#!/usr/bin/python
# encoding: utf-8
# -*- coding: utf8 -*-
import os
import re
import sys

try:
    import platform
except ImportError:
    try:
        command_to_execute = "pip install platform || easy_install platform"
        os.system(command_to_execute)
    except OSError:
        print("Can NOT install 'platform', Aborted!")
        sys.exit(1)
    except Exception as e:
        print("Uncaught exception, %s" % str(e))
        sys.exit(1)
    import platform

print(platform.uname())
if platform.linux_distribution()[0] == "":
    pass
else:
    print(platform.linux_distribution())
print(platform.system())
print(platform.platform())
print(platform.architecture())
print(platform.version())
print(platform.release())
print(platform.node())
print(platform.machine())
print(platform.win32_ver())

print(os.name)
print(sys.platform)

if 'nt' in os.name:
    print('Windows')
elif 'posix' in os.name:
    print('Linux')

try:
    with open('/etc/issue') as f:
        content = f.read().lower().strip()
        output_list = re.split(r' ', content)
        linux_type = list(output_list)[0]
except IOError:
    pass
else:
    if linux_type is not None:
        print(linux_type)
