#!/usr/bin/python
# encoding: utf-8
# -*- coding: utf8 -*-
"""
Created by PyCharm.
File:               LinuxBashShellScriptForOps:getPortFromFileOnLinux.py
User:               Guodong
Create Date:        2016/9/23
Create Time:        15:05
 """
import re
import os


def int2hex(number):
    if number > 65535:
        print("accepted number should little than 65535.")
        raise RuntimeError
    result = hex(number)
    tmp = str(result).split('0x')[1]
    if len(tmp) == 1:
        return "000" + tmp
    elif len(tmp) == 2:
        return "00" + tmp
    elif len(tmp) == 3:
        return "0" + tmp
    elif len(tmp) == 4:
        return tmp


pid = 1293
port = 22
port_16 = int2hex(port)

if os.path.exists("/proc/net/tcp"):
    with open("/proc/net/tcp", 'r') as f:
        tcp = f.read()
    if tcp is not None and tcp != "":
        pattern = re.compile(".*:" + port_16 + ".*\n")
        match = pattern.search(tcp)
        if match:
            line = match.group()
            if line is not None and line != "":
                line = ' '.join([x for x in line.split(' ') if x])
                socket_fd = line.split(' ')[9]
                port_hex = line.split(' ')[1].split(':')[1]
                port = int(port_hex, 16)

fd_dir = "/proc/%s/fd" % pid
files = os.listdir(fd_dir)
fd_real_name = list()
for f in files:
    if socket_fd in str(os.readlink(os.path.join(fd_dir, f))):
        print("pid %s is using port %s, and socket id is %s" % (pid, port, socket_fd))
    else:
        print("pid %s not is using port %s" % (pid, port))
