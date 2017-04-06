#!/usr/bin/python
# encoding: utf-8
# -*- coding: utf8 -*-
"""
Created by PyCharm.
File:               LinuxBashShellScriptForOps:getSshPublicFingerprint.py
User:               Guodong
Create Date:        2017/3/21
Create Time:        19:16
 """
# Goal:
# Show fingerprint of key file.
# same as `ssh-keygen -l`

# http://stackoverflow.com/questions/12196700/python-paramiko-verifying-ssh-host-key-fingerprints-manually
# python  show fingerprint of key file
# https://gist.github.com/jtriley/7270594
# https://www.example-code.com/python/ssh_key_fingerprint.asp
# http://stackoverflow.com/questions/6682815/deriving-an-ssh-fingerprint-from-a-public-key-in-python/6682934#6682934
# http://sharadchhetri.com/2013/06/03/how-to-know-public-key-fingerprint/
import paramiko
import binascii

hostname = "192.168.1.1"
port = 22
username = "ubnt"
password = ""
if password == "":
    password = raw_input("Please input password for %s@%s: " % (username, hostname))
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(hostname=hostname, port=port, username=username, password=password)
keys = ssh.get_host_keys()
key = keys['192.168.1.1']['ssh-rsa']
print binascii.hexlify(key.get_fingerprint())
ssh.close()
