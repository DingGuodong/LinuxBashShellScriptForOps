#!/usr/bin/python
# encoding: utf-8
# -*- coding: utf8 -*-
"""
Created by PyCharm.
File:               LinuxBashShellScriptForOps:remove_blank_line.py
User:               Guodong
Create Date:        2016/9/6
Create Time:        14:14
 """

import os

filename = "exampleFile.txt"
if os.path.exists(os.path.join(os.path.dirname(os.path.abspath(__file__)), filename)):
    with open(filename) as f:
        for each_line in f:
            if each_line[:-1].strip() == "":
                pass
            else:
                print(each_line[:-1])
