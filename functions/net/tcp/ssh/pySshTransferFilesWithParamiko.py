#!/usr/bin/python
# encoding: utf-8
# -*- coding: utf-8 -*-
"""
Created by PyCharm.
File Name:              LinuxBashShellScriptForOps:pySshTransferFilesWithParamiko.py
Version:                0.0.1
Author:                 Guodong
Author Email:           dgdenterprise@gmail.com
URL:                    https://github.com/DingGuodong/LinuxBashShellScriptForOps
Download URL:           https://github.com/DingGuodong/LinuxBashShellScriptForOps/tarball/master
Create Date:            2018/10/26
Create Time:            17:02
Description:            python transfer files with paramiko module over SSH protocol
Long Description:       
References:             
Prerequisites:          []
Development Status:     3 - Alpha, 5 - Production/Stable
Environment:            Console
Intended Audience:      System Administrators, Developers, End Users/Desktop
License:                Freeware, Freely Distributable
Natural Language:       English, Chinese (Simplified)
Operating System:       POSIX :: Linux, Microsoft :: Windows
Programming Language:   Python :: 3

Topic:                  Utilities
 """
import paramiko

hostname = "120.27.194.133"
port = paramiko.config.SSH_PORT
username = 'root'
password = None
key_filename = r"C:\Users\Guodong\.ssh\ebt-linux-centos-ssh-root-key.pem"
timeout = 5

# making a connection with accept host key
ssh_client = paramiko.SSHClient()
ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh_client.connect(hostname, port=port, username=username, key_filename=key_filename, timeout=timeout)

# file transfers
sftp_client = ssh_client.open_sftp()
sftp_client.get('/root/.bash_profile', '.bash_profile')  # Downloading a file from remote machine
sftp_client.put(__file__, 'this.py')  # Uploading file from local to remote machine

# running commands on the remote machine
stdin, stdout, stderr = ssh_client.exec_command("ls this.py && pwd")
print(stdout.read())
stdin.close()
stdout.close()
stderr.close()

# commands requiring input
stdin, stdout, stderr = ssh_client.exec_command("rm this.py")
stdin.write("y")
print(stderr.read())
stdin.close()
stdout.close()
stderr.close()

sftp_client.close()

ssh_client.close()
