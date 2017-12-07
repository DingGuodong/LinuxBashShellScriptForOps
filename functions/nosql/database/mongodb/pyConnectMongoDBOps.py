#!/usr/bin/python
# encoding: utf-8
# -*- coding: utf8 -*-
"""
Created by PyCharm.
File Name:              LinuxBashShellScriptForOps:pyConnectMongoDBOps.py
Version:                0.0.1
Author:                 Guodong
Author Email:           dgdenterprise@gmail.com
URL:                    https://github.com/DingGuodong/LinuxBashShellScriptForOps
Download URL:           https://github.com/DingGuodong/LinuxBashShellScriptForOps/tarball/master
Create Date:            2017/12/7
Create Time:            13:57
Description:            use python operate MongoDB
Long Description:       
References:             https://docs.mongodb.com/getting-started/python/client/
                        https://docs.mongodb.com/getting-started/python/
                        http://api.mongodb.com/python/current/api/pymongo/mongo_client.html#pymongo.mongo_client.MongoClient
Prerequisites:          []
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
from pymongo import MongoClient

client = MongoClient("mongodb://10.45.51.99:27017")

# use 'usertrack' database
db = client.usertrack

# list tables
print db.collection_names()

# show column counts of table 'usertrack' in db 'usertrack'
print db.usertrack.count()

# show records of table 'usertrack' in db 'usertrack'
cursor = db.usertrack.find()
for document in cursor:
    print(document)

# show records of table 'uservisit' in db 'usertrack'
cursor = db.uservisit.find()
for document in cursor:
    print(document)

# show data by "visitId"
cursor = db.uservisit.find({"visitId": "34BBF86A-1BB6-4D69-B851-AC5E45182957"})
for document in cursor:
    print(document)
