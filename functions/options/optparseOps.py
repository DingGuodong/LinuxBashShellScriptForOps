#!/usr/bin/python
# encoding: utf-8
# -*- coding: utf8 -*-
"""
Created by PyCharm.
File:               LinuxBashShellScriptForOps:optparseOps.py
User:               Guodong
Create Date:        2016/12/12
Create Time:        16:46
 """
import optparse

parser = optparse.OptionParser()

parser.add_option('-q', '--query',
                  action="store", dest="query",
                  help="query string", default="spam")

options, args = parser.parse_args()

print 'Query string:', options.query
