#!/usr/bin/python
# encoding: utf-8
# -*- coding: utf8 -*-
"""
Created by PyCharm.
File:               LinuxBashShellScriptForOps:pyConnectOracle.py
User:               Guodong
Create Date:        2016/11/24
Create Time:        10:39
 """
import cx_Oracle as orcl

print(orcl.clientversion())
username = "system"
password = "oracle"
host = "localhost"
port = "1521"
sid = "xe"

dsn = orcl.makedsn(host, port, sid)
con = orcl.connect(username, password, dsn)
cursor = con.cursor()
sql = "SELECT * FROM HELP"
cursor.execute(sql)
result = cursor.fetchall()
print("Total: " + str(cursor.rowcount))
for row in result:
    print(row)
cursor.close()
con.close()
