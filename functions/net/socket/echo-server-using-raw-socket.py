#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created by PyCharm.
File Name:              LinuxBashShellScriptForOps:echo-server-using-raw-socket.py
Version:                0.0.1
Author:                 dgden
Author Email:           dgdenterprise@gmail.com
URL:                    https://github.com/DingGuodong/LinuxBashShellScriptForOps
Download URL:           https://github.com/DingGuodong/LinuxBashShellScriptForOps/tarball/master
Create Date:            2020/8/12
Create Time:            15:22
Description:            echoes all data that it receives back (servicing only one client)
Long Description:       
References:             https://docs.python.org/3/library/socket.html
                        https://docs.python.org/3/library/socket.html#example
                        [Python Socket Multiple Clients](https://stackoverflow.com/questions/10810249/python-socket-multiple-clients)
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
import sys

import socket
# import thread
import threading

# host is a domain name, a string representation of an IPv4/v6 address or None.
HOST = None  # '0.0.0.0'(IPv4)  # Symbolic name meaning all available interfaces

# port is a string service name such as 'http', a numeric port number or None.
PORT = 50007  # Arbitrary non-privileged port

s = None
for res in socket.getaddrinfo(HOST, PORT, socket.AF_UNSPEC,
                              socket.SOCK_STREAM, 0, socket.AI_PASSIVE):
    af, socktype, proto, canonname, sa = res
    try:
        s = socket.socket(af, socktype, proto)
    except OSError as msg:
        s = None
        continue
    try:
        s.bind(sa)
        s.listen(1)
        print("Port {port} is listened, try with 'telnet {host} {port}'".format(port=sa[1], host=sa[0]))
    except OSError as msg:
        s.close()
        s = None
        continue
    break

if s is None:
    print('could not open socket')
    sys.exit(1)


def conn_handler(cur_conn, cur_addr):
    print('Connected by', cur_addr)
    while True:
        data = cur_conn.recv(1024)
        if not data:
            break
        cur_conn.send(data)


while True:
    # blocking until accept one client
    conn, addr = s.accept()

    # thread.start_new_thread(conn_handler, (conn, addr))
    # thread._count()
    threading.Thread(target=conn_handler, args=(conn, addr)).start()
    print(threading.active_count())
