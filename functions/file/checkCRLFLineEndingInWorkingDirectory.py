#!/usr/bin/python
# encoding: utf-8
# -*- coding: utf8 -*-
"""
Created by PyCharm.
File:               LinuxBashShellScriptForOps:checkCRLFLineEndingInWorkingDirectory.py
User:               Guodong
Create Date:        2017/7/14
Create Time:        14:24
Description:        find out all files using CRLF line ending
References:         
 """

import os


def checkCRLFLineEnding(path):
    with open(path, 'rb') as f:
        content = f.readlines()
        if len(content) > 1:
            if content[0].endswith('\r\n'):
                return True
            else:
                return False
        else:
            print "Empty file {file}".format(file=path)
            return False


if __name__ == '__main__':
    file_extension_list = ['.sh', '.py', '.md']
    working_directory = r'C:\Users\Guodong\PycharmProjects\LinuxBashShellScriptForOps'
    # TODO(Guodong Ding) use gevent or multi-threading will get better performance
    for top, dirs, nondirs in os.walk(working_directory):
        if len(nondirs) != 0:
            for filename in nondirs:
                full_path_to_filename = os.path.join(top, filename)
                if full_path_to_filename.endswith(tuple([ext for ext in file_extension_list])):
                    if checkCRLFLineEnding(full_path_to_filename):
                        print full_path_to_filename
