#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created by PyCharm.
File Name:              LinuxBashShellScriptForOps:find-host-which-port-opened.py
Version:                0.0.1
Author:                 dgden
Author Email:           dgdenterprise@gmail.com
URL:                    https://github.com/DingGuodong/LinuxBashShellScriptForOps
Download URL:           https://github.com/DingGuodong/LinuxBashShellScriptForOps/tarball/master
Create Date:            2021/6/24
Create Time:            20:07
Description:            find the host which a port is opened.
Long Description:       
References:             
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
import ipaddress


def is_port_open(host, port):
    """
    :param host: str
    :param port:  int
    :return:  boolean
    """

    import socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(1)
    try:
        s.connect((host, int(port)))
        s.shutdown(socket.AF_INET)
        return True
    except socket.error:
        return False
    finally:
        s.close()


if __name__ == '__main__':
    network = ipaddress.ip_network(u"192.168.1.0/24")
    for ip in network.hosts():
        if is_port_open(str(ip), 3389):
            print(ip)
