#!/usr/bin/python
# encoding: utf-8
# -*- coding: utf8 -*-
"""
Created by PyCharm.
File:               LinuxBashShellScriptForOps:pyParseYamlFile.py
User:               Guodong
Create Date:        2017/1/19
Create Time:        11:50

References on Website:
    http://yaml.org/
    http://pyyaml.org/
    http://pyyaml.org/wiki/PyYAMLDocumentation

 """
from yaml import load, dump

try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper

document = """
  a: 1
  b:
    c: 3
    d: 4
"""

print dump(load(document), default_flow_style=False)
print load(document)
