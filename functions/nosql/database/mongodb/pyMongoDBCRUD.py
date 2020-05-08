#!/usr/bin/python
# encoding: utf-8
# -*- coding: utf-8 -*-
"""
Created by PyCharm.
File Name:              LinuxBashShellScriptForOps:pyMongoDBCRUD.py
Version:                0.0.1
Author:                 Guodong
Author Email:           dgdenterprise@gmail.com
URL:                    https://github.com/DingGuodong/LinuxBashShellScriptForOps
Download URL:           https://github.com/DingGuodong/LinuxBashShellScriptForOps/tarball/master
Create Date:            2018/8/8
Create Time:            20:17
Description:            
Long Description:       # Back Up and Restore with MongoDB Tools
                        # https://docs.mongodb.com/manual/tutorial/backup-and-restore-tools/
                        mongodump -d usertrack --gzip --archive=usertrack.bson.gz
                        mongorestore --gzip --archive=usertrack.bson.gz -d usertrack

                        # The GUI for MongoDB
                        MongoDB Compass Community
                        https://www.mongodb.com/products/compass

References:             
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

import datetime
import time

from dateutil.relativedelta import relativedelta  # pip install -U python-dateutil
from pymongo import MongoClient

client = MongoClient("mongodb://127.0.0.1:27017")

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
    print(type(document))
    print("{:16.1f}".format(dict(document).get('actionTime')))
    break

# delete records of table 'usertrack' in db 'usertrack'
save_days = 30
timestamp_before_save_days = time.mktime((datetime.datetime.today() + relativedelta(days=-save_days)).timetuple())
javascript_timestamp = timestamp_before_save_days * 1000
print(str(javascript_timestamp))

usertrack = db.usertrack
print(usertrack.find_one())

result = usertrack.find({"actionTime": {"$lt": javascript_timestamp}}).count()
print(result)

# result = usertrack.remove({"actionTime": {"$lt": javascript_timestamp}})
# print(result)
#
# result = usertrack.delete_many({"actionTime": {"$lt": javascript_timestamp}})
# print(result.deleted_count)
