#!/usr/bin/python
# encoding: utf-8
# -*- coding: utf8 -*-
"""
Created by PyCharm.
File:               LinuxBashShellScriptForOps:getoptOps.py
User:               Guodong
Create Date:        2016/9/20
Create Time:        14:27
 """
import sys
import getopt
import os


def usage():
    print "%s -h    show this help message." % os.path.basename(sys.argv[0])
    print "%s -i    do something." % os.path.basename(sys.argv[0])
    print "%s -o    do something else." % os.path.basename(__file__)


para_i = ""
para_o = ""
opts, args = getopt.getopt(sys.argv[1:], "hi:o:", ["help", "input=", "output="])
for opt, value in opts:
    if opt == "-i" or opt in "--input":
        para_i = value
    elif opt == "-o" or opt in "--output":
        para_o = value
    elif opt == "-h" or opt in "--help":
        usage()
        sys.exit(0)

if para_i != "":
    print "%s reverse is %s" % ("para_i", para_i[::-1])

if para_o != "":
    print "%s reverse is %s" % ("para_o", para_o[::-1])
