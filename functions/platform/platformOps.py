#!/usr/bin/python
# -*- coding: utf-8 -*-
# Do not reinventing the wheel
import platform
import sys

# platform.platform()
# platform.version()
# platform.architecture()
# platform.machine()
# platform.node()
# platform.processor()
# platform.uname()

os_type = platform.uname()[0]

if os_type == "Linux":
    print "Linux"
elif os_type == "Windows":
    print "Windows"
else:
    exit("Unknown Operating System!")

print sys.version_info
print sys.platform
