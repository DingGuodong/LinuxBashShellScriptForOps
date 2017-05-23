#!/usr/bin/python
# encoding: utf-8
# -*- coding: utf8 -*-
"""
Created by PyCharm.
File:               LinuxBashShellScriptForOps:pySshConnectOps.py
User:               Guodong
Create Date:        2016/12/23
Create Time:        11:10
 """
import paramiko

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect("10.6.28.36", port=20122, username="root", key_filename="id_rsa", timeout=2)
stdin, stdout, stderr = client.exec_command("uname -a")
for line in stdout:
    print line,
client.close()
