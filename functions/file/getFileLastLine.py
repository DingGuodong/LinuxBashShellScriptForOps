#!/usr/bin/python
# encoding: utf-8
# -*- coding: utf8 -*-
"""
Created by PyCharm.
File:               LinuxBashShellScriptForOps:get-last-line-of-file.py
User:               Guodong
Create Date:        2016/9/1
Create Time:        11:05
 """
import os


# Refer: http://www.pythonclub.org/python-files/last-line
def get_last_line(path):
    file_size = os.path.getsize(path)
    block_size = 1024
    dat_file = open(path, 'rb')
    last_line = ""
    if file_size > block_size:
        max_seek_point = (file_size // block_size)
        dat_file.seek((max_seek_point - 1) * block_size)
    elif file_size:
        # max_seek_point = block_size % file_size
        dat_file.seek(0, 0)
    lines = dat_file.readlines()
    if lines:
        last_line = lines[-1].strip()
    # print "last line : ", last_line
    dat_file.close()
    return last_line


# Refer: http://code.activestate.com/recipes/578095/
def print_first_last_line(path):
    file_size = os.path.getsize(path)
    block_size = 1024
    dat_file = open(path, 'rb')
    headers = dat_file.readline().strip()
    if file_size > block_size:
        max_seek_point = (file_size // block_size)
        dat_file.seek(max_seek_point * block_size)
    elif file_size:
        max_seek_point = block_size % file_size
        dat_file.seek(max_seek_point)
    lines = dat_file.readlines()
    last_line = ""
    if lines:
        last_line = lines[-1].strip()
    # print "first line : ", headers
    # print "last line : ", last_line
    return headers, last_line


# My Implementation
def get_file_last_line(path):
    file_size = os.path.getsize(path)
    block_size = 1024
    with open(path, 'rb') as f:
        last_line = ""
        if file_size > block_size:
            max_seek_point = (file_size // block_size)
            f.seek((max_seek_point - 1) * block_size)
        elif file_size:
            f.seek(0, 0)
        lines = f.readlines()
        if lines:
            lineno = 1
            while last_line == "":
                last_line = lines[-lineno].strip()
                lineno += 1
        return last_line


if __name__ == '__main__':
    # Test purpose
    print(get_last_line(os.path.abspath(__file__)))
    print(print_first_last_line(os.path.abspath(__file__)))
    print(get_file_last_line(os.path.abspath(__file__)))
