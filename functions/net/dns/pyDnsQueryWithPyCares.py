#!/usr/bin/python
# encoding: utf-8
# -*- coding: utf-8 -*-
"""
Created by PyCharm.
File Name:              LinuxBashShellScriptForOps:pyDnsQueryWithPyCares.py
Version:                0.0.1
Author:                 Guodong
Author Email:           dgdenterprise@gmail.com
URL:                    https://github.com/DingGuodong/LinuxBashShellScriptForOps
Download URL:           https://github.com/DingGuodong/LinuxBashShellScriptForOps/tarball/master
Create Date:            2018/9/10
Create Time:            14:57
Description:            
Long Description:       
References:             https://github.com/saghul/pycares/blob/master/examples/cares-select.py
                        https://pycares.readthedocs.io/en/latest/channel.html#
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

import select
import socket

import pycares


def wait_channel(channel):
    while True:
        read_fds, write_fds = channel.getsock()
        if not read_fds and not write_fds:
            break
        timeout = channel.timeout()
        if not timeout:
            channel.process_fd(pycares.ARES_SOCKET_BAD, pycares.ARES_SOCKET_BAD)
            continue
        rlist, wlist, xlist = select.select(read_fds, write_fds, [], timeout)
        for fd in rlist:
            channel.process_fd(fd, pycares.ARES_SOCKET_BAD)
        for fd in wlist:
            channel.process_fd(pycares.ARES_SOCKET_BAD, fd)


if __name__ == '__main__':
    def cb(result, error):
        print(result)
        if error:
            print(error)

    current_channel = pycares.Channel()
    current_channel.gethostbyname('google.com', socket.AF_INET, cb)
    current_channel.query('www.taobao.com', pycares.QUERY_TYPE_A, cb)
    current_channel.query('sip2sip.info', pycares.QUERY_TYPE_SOA, cb)
    wait_channel(current_channel)

    print("Done!")
