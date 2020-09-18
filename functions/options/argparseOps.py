#!/usr/bin/python
# encoding: utf-8
# -*- coding: utf8 -*-
"""
Created by PyCharm.
File:               LinuxBashShellScriptForOps:argparseOps.py
User:               Guodong
Create Date:        2016/9/20
Create Time:        15:02
References:         [argparse](https://docs.python.org/zh-cn/3/library/argparse.html)
 """
import argparse

parser = argparse.ArgumentParser(description='show argparse example')

parser.add_argument('integers', metavar='Number', type=int, nargs='+',
                    help='an integer for the accumulator')

parser.add_argument('--sum', dest='accumulate', action='store_const',
                    const=sum, default=max,
                    help='sum the integers (default: find the max)')

parser.add_argument('--t1', '-t', nargs='*', help='desc')
parser.add_argument('--t2', '-T', nargs='+', help='desc')  # expected at least one argument

parser.add_argument('--t3', nargs='?', help='desc')  # expected 0 or 1 argument

# [metavar](https://docs.python.org/zh-cn/3/library/argparse.html#metavar)
parser.add_argument('--t4-s1', nargs='*', metavar='para', help='desc')  # argument will be saved to t4_s1

# [dest](https://docs.python.org/zh-cn/3/library/argparse.html#dest)
parser.add_argument('--t5-s2', dest='para1', nargs='*', metavar='para')  # argument will be saved to para1

# [type](https://docs.python.org/zh-cn/3/library/argparse.html#type)
parser.add_argument('--t6', dest='para1', type=int, nargs='*', metavar='para')  # argument will be saved to para1

args = parser.parse_args()  # '-h' or '--help' will stop here and exit 0.
print(args)
print(args.integers)
print(args.t1)
