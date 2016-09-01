#!/usr/bin/python
# encoding: utf-8
# -*- coding: utf8 -*-
"""
Created by PyCharm.
File:               LinuxBashShellScriptForOps:getFileLastLine.py
User:               Guodong
Create Date:        2016/9/1
Create Time:        11:05
 """
import os


# Refer: http://www.pythonclub.org/python-files/last-line
def get_last_line(inputfile):
    filesize = os.path.getsize(inputfile)
    blocksize = 1024
    dat_file = open(inputfile, 'rb')
    last_line = ""
    if filesize > blocksize:
        maxseekpoint = (filesize // blocksize)
        dat_file.seek((maxseekpoint - 1) * blocksize)
    elif filesize:
        # maxseekpoint = blocksize % filesize
        dat_file.seek(0, 0)
    lines = dat_file.readlines()
    if lines:
        last_line = lines[-1].strip()
    # print "last line : ", last_line
    dat_file.close()
    return last_line


# Refer: http://code.activestate.com/recipes/578095/
def print_first_last_line(inputfile):
    filesize = os.path.getsize(inputfile)
    blocksize = 1024
    dat_file = open(inputfile, 'rb')
    headers = dat_file.readline().strip()
    if filesize > blocksize:
        maxseekpoint = (filesize // blocksize)
        dat_file.seek(maxseekpoint * blocksize)
    elif filesize:
        maxseekpoint = blocksize % filesize
        dat_file.seek(maxseekpoint)
    lines = dat_file.readlines()
    if lines:
        last_line = lines[-1].strip()
    # print "first line : ", headers
    # print "last line : ", last_line
    return headers, last_line


# My Implementation
def get_file_last_line(inputfile):
    filesize = os.path.getsize(inputfile)
    blocksize = 1024
    with open(inputfile, 'rb') as f:
        last_line = ""
        if filesize > blocksize:
            maxseekpoint = (filesize // blocksize)
            f.seek((maxseekpoint - 1) * blocksize)
        elif filesize:
            f.seek(0, 0)
        lines = f.readlines()
        if lines:
            lineno = 1
            while last_line == "":
                last_line = lines[-lineno].strip()
                lineno += 1
        return last_line

# Test purpose
# print get_last_line(os.path.abspath(__file__))
# print print_first_last_line(os.path.abspath(__file__))
# print get_file_last_line(os.path.abspath(__file__))
