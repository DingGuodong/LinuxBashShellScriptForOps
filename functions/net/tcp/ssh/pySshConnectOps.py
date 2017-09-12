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
client.connect("120.27.194.133", port=22, username="root",
               key_filename="C:\Users\Guodong\.ssh\ebt-linux-centos-ssh-root-key.pem", timeout=5)

# TODO(Guodong Ding) paramiko add customized environment issue, next line not works on centos and ubuntu
stdin, stdout, stderr = client.exec_command('echo "x$user_defined_variable_name"',
                                            environment={"user_defined_variable_name": "1"}, get_pty=True)
for line in stdout:
    print line,
client.close()
