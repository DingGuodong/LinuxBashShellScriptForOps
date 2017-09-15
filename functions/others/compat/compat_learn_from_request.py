#!/usr/bin/python
# encoding: utf-8
# -*- coding: utf8 -*-
"""
Created by PyCharm.
File:               LinuxBashShellScriptForOps:compat_learn_from_request.py
User:               Guodong
Create Date:        2017/9/15
Create Time:        11:07
Description:        
References:         https://github.com/requests/requests/blob/master/requests/compat.py
Prerequisites:      []
 """
# -*- coding: utf-8 -*-

"""
requests.compat
~~~~~~~~~~~~~~~
This module handles import compatibility issues between Python 2 and
Python 3.
"""

import sys

# -------
# Pythons
# -------

# Syntax sugar.
_ver = sys.version_info

#: Python 2.x?
is_py2 = (_ver[0] == 2)

#: Python 3.x?
is_py3 = (_ver[0] == 3)

try:
    import simplejson as json
except ImportError:
    import json

# ---------
# Specifics
# ---------

if is_py2:
    pass

elif is_py3:
    pass
