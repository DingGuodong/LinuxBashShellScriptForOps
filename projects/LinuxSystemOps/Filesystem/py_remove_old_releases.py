#!/usr/bin/python
# encoding: utf-8
# -*- coding: utf8 -*-
"""
Created by PyCharm.
File Name:              LinuxBashShellScriptForOps:py_remove_old_releases.py
Version:                0.0.1
Author:                 Guodong
Author Email:           dgdenterprise@gmail.com
URL:                    https://github.com/DingGuodong/LinuxBashShellScriptForOps
Download URL:           https://github.com/DingGuodong/LinuxBashShellScriptForOps/tarball/master
Create Date:            2017/11/22
Create Time:            10:42
Description:            remove old releases which deployed into multi-part places
Long Description:       
References:             
Prerequisites:          shutil
Development Status:     3 - Alpha, 5 - Production/Stable
Environment:            Console
Intended Audience:      System Administrators, Developers, End Users/Desktop
License:                Freeware, Freely Distributable
Natural Language:       English, Chinese (Simplified)
Operating System:       POSIX :: Linux, Microsoft :: Windows
Programming Language:   Python :: 3

Topic:                  Utilities
 """
import os
import shutil
import time

releases_save_size = 10

services_releases_to_clean_dict = {
    "releases": [
        {
            "path": "/tmp",  # one path to deploy
            "type": "d"  # file type to clean, 'd' means directory, 'f' means file
        },
        {
            "path": "/opt/ebt/apps",
            "type": "d"
        },
        {
            "path": "/opt/ebt/apps/app-files",
            "type": "f"
        },
    ]
}

services_list = [  # put your service name here, filename starts with this service name will be handled
    r'agent-management',
    r'agent-stats',
    r'canal-to-kafka',
    r'car',
    r'cashier',
    r'customer',
    r'dataexchange',
    r'ebtdatres',
    r'erisk',
    r'erp',
    r'insiap',
    r'insure-validation',
    r'jetty-docbase',
    r'message',
    r'policy',
    r'proposal',
    r'resource',
    r'risk-market',
    r'sms',
    r'user',
    r'zyj-touch',
    r'zy-cloud',
]

print("WARNING: files as follows will be deleted, this is unrecoverable.")
print("=" * 64)

for service in services_list:
    for release in services_releases_to_clean_dict["releases"]:
        path = release.get("path")
        file_type = release.get("type")
        all_files_with_date_dict = dict()

        if os.path.exists(path):
            # get the files list ready
            for top, dirs, nondirs in os.walk(path):
                if file_type == 'f':
                    if len(nondirs) != 0:
                        for filename in nondirs:
                            # TODO(GuodongDing) if there are many services will lead to low performance
                            if filename.startswith(service):
                                full_path_to_file = os.path.join(top, filename)
                                # print full_path_to_file
                                all_files_with_date_dict[full_path_to_file] = os.path.getctime(full_path_to_file)
                elif file_type == 'd':
                    if len(dirs) != 0:
                        for directory in dirs:
                            if directory.startswith(service):
                                full_path_to_file = os.path.join(top, directory)
                                # print full_path_to_file
                                all_files_with_date_dict[full_path_to_file] = os.path.getmtime(
                                    full_path_to_file)  # ready for ls -t, sort by modification time
                break  # max depth = 1

            # delete files if releases count large then 5
            if len(list(all_files_with_date_dict.items())) > releases_save_size:
                for item in sorted(list(all_files_with_date_dict.items()), key=lambda x: x[1],
                                   reverse=True)[releases_save_size::]:  # ls -t, sort by modification time
                    filename = item[0]
                    if os.path.exists(filename):

                        if os.path.isdir(filename):
                            print("[D]: ", filename, "; Last modify time: ", time.strftime('%Y-%m-%d %H:%M:%S',
                                                                                           time.localtime(item[1])))
                            shutil.rmtree(filename)
                        elif os.path.isfile(filename):
                            print("[F]: ", filename, "; Last modify time: ", time.strftime('%Y-%m-%d %H:%M:%S',
                                                                                           time.localtime(item[1])))
                            os.remove(filename)

print("=" * 64)
print("SUCCESS: clean finished")
