#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created by PyCharm.
File Name:              LinuxBashShellScriptForOps:py-connect-mongodb-quick-start.py
Version:                0.0.1
Author:                 dgden
Author Email:           dgdenterprise@gmail.com
URL:                    https://github.com/DingGuodong/LinuxBashShellScriptForOps
Download URL:           https://github.com/DingGuodong/LinuxBashShellScriptForOps/tarball/master
Create Date:            2019/6/4
Create Time:            17:59
Description:            
Long Description:       
References:             http://docs.mongoengine.org/guide/connecting.html
                        https://github.com/MongoEngine/mongoengine
Prerequisites:          pip2 install mongoengine
Development Status:     3 - Alpha, 5 - Production/Stable
Environment:            Console
Intended Audience:      System Administrators, Developers, End Users/Desktop
License:                Freeware, Freely Distributable
Natural Language:       English, Chinese (Simplified)
Operating System:       POSIX :: Linux, Microsoft :: Windows
Programming Language:   Python :: 2.6
Programming Language:   Python :: 2.7
Topic:                  Utilities
 """

from mongoengine import connect

# client = connect('usertrack', host="mongodb://127.0.0.1:27017")
client = connect(db='usertrack', host="127.0.0.1", port=27017)
server_info = client.server_info()
print(server_info.get('version'))
