#!/usr/bin/python
# encoding: utf-8
# -*- coding: utf8 -*-
"""
Created by PyCharm.
File:               LinuxBashShellScriptForOps:simpleSysArgsExamples.py
User:               Guodong
Create Date:        2017/7/7
Create Time:        9:30
Description:        
 """
import sys


def process_one_fixed_para(num):
    print num


def process_more_than_one_not_fixed_para_without_key(num, *args):
    print num, args


def process_more_than_one_not_fixed_para_with_key(num, *args, **kwargs):
    print num, args, kwargs


if __name__ == '__main__':
    if len(sys.argv) > 1:
        print "got %s" % sys.argv[1]
        process_one_fixed_para(len(sys.argv))
        process_more_than_one_not_fixed_para_without_key(len(sys.argv), sys.argv)
        process_more_than_one_not_fixed_para_with_key(len(sys.argv), sys.argv, {'length': len(sys.argv)}, )
    else:
        print "got %s" % sys.argv
