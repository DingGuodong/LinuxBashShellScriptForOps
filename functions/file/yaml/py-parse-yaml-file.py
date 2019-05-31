#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created by PyCharm.
File Name:              LinuxBashShellScriptForOps:py-parse-yaml-file.py
Version:                0.0.1
Author:                 Guodong
Author Email:           dgdenterprise@gmail.com
URL:                    https://github.com/DingGuodong/LinuxBashShellScriptForOps
Download URL:           https://github.com/DingGuodong/LinuxBashShellScriptForOps/tarball/master
Create Date:            2019/3/22
Create Time:            14:25
Description:            
Long Description:       
References:             
Prerequisites:          pip install PyYAML
Development Status:     3 - Alpha, 5 - Production/Stable
Environment:            Console
Intended Audience:      System Administrators, Developers, End Users/Desktop
License:                Freeware, Freely Distributable
Natural Language:       English, Chinese (Simplified)
Operating System:       POSIX :: Linux, Microsoft :: Windows
Programming Language:   Python :: 3
Topic:                  Utilities
 """

import requests

try:
    import cStringIO as StringIO
except ImportError:
    import StringIO

import yaml
import json


yml_url = u'https://raw.githubusercontent.com/pallets/flask/master/.travis.yml'

yml_content = requests.get(yml_url).content


yml_io_buffer = StringIO.StringIO(yml_content)


yml_dict = yaml.load(yml_content)

# helper for read python dict object
print(json.dumps(yml_dict, indent=4))
