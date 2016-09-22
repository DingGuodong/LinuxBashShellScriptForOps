#!/usr/bin/python
# encoding: utf-8
# -*- coding: utf8 -*-
"""
Created by PyCharm.
File:               LinuxBashShellScriptForOps:argparseOps.py
User:               Guodong
Create Date:        2016/9/20
Create Time:        15:02
 """
import argparse

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('integers', metavar='N', type=int, nargs='+',
                    help='an integer for the accumulator')
parser.add_argument('--sum', dest='accumulate', action='store_const',
                    const=sum, default=max,
                    help='sum the integers (default: find the max)')

args = parser.parse_args()
print args.accumulate(args.integers)
