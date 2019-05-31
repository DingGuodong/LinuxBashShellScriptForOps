#!/usr/bin/python
# encoding: utf-8
# -*- coding: utf8 -*-
"""
Created by PyCharm.
File:               LinuxBashShellScriptForOps:pySortFiles.py
User:               Guodong
Create Date:        2017/7/17
Create Time:        11:07
Description:        python sort files with ctime
References:         http://python.jobbole.com/85124/
 """
import os

if __name__ == '__main__':
    file_extension_list = ['.sh', '.py', '.md']
    working_directory = r'C:\Users\Guodong\PycharmProjects\LinuxBashShellScriptForOps'
    all_files_with_date_dict = dict()
    for top, dirs, nondirs in os.walk(working_directory):
        if len(nondirs) != 0:
            for filename in nondirs:
                full_path_to_filename = os.path.join(top, filename)
                if full_path_to_filename.endswith(tuple(file_extension_list)):
                    all_files_with_date_dict[full_path_to_filename] = os.path.getctime(full_path_to_filename)
    for item in sorted(all_files_with_date_dict.items(), key=lambda x: x[1], reverse=True):
        print(item[0])
