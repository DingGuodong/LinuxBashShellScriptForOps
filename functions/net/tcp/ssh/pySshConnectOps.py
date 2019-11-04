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
client.connect("192.168.88.19", port=22, username="root",
               key_filename=r"C:\Users\dgden\.ssh\exportedkey201310171355", timeout=5)


stdin, stdout, stderr = client.exec_command('echo "x$user_defined_variable_name x"',
                                            environment={"user_defined_variable_name": "1"}, get_pty=True)
"""
warning::   
            The server may reject this request depending on its ``AcceptEnv``
            setting; such rejections will fail silently (which is common client
            practice for this particular request type). Make sure you
            understand your server's configuration before using!
"""
for line in stdout:
    print line,
client.close()
