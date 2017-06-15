#!/usr/bin/python
# encoding: utf-8
# -*- coding: utf8 -*-
"""
Created by PyCharm.
File:               LinuxBashShellScriptForOps:pyTelnetOps.py
User:               Guodong
Create Date:        2017/6/15
Create Time:        16:14
 """
import telnetlib

host = '192.168.88.1'
username = 'username'
password = 'password'
finish = 'SSG140->'
command = 'ping 192.168.88.11'
command_to_exit = 'exit'

tn = telnetlib.Telnet(host)
tn.set_debuglevel(2)

tn.read_until('login:')
tn.write(username + '\n')

tn.read_until('password:')
tn.write(password + '\n')

tn.read_until(finish)

tn.write(command + '\n')

tn.read_until(finish)

tn.write(command_to_exit + '\n')
tn.close()
