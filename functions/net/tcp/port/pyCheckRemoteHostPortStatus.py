#!/usr/bin/python
# encoding: utf-8
# -*- coding: utf8 -*-
"""
Created by PyCharm.
File Name:              LinuxBashShellScriptForOps:pyCheckRemoteHostPortStatus.py
Version:                0.0.1
Author:                 Guodong
Author Email:           dgdenterprise@gmail.com
URL:                    https://github.com/DingGuodong/LinuxBashShellScriptForOps
Download URL:           https://github.com/DingGuodong/LinuxBashShellScriptForOps/tarball/master
Create Date:            2017/12/28
Create Time:            10:19
Description:            check remote host's tcp port if is open, U2
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
import time


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
    hostname_to_test = '127.0.0.1'
    port_to_test = 3389

    try:
        print("checking ...")
        keep_running_flag = True
        while keep_running_flag:
            if is_port_open(hostname_to_test, port_to_test):
                keep_running_flag = False
            else:
                print("port is not opened")
                time.sleep(1)

        print("port {port} on host {host} is opened".format(port=port_to_test, host=hostname_to_test))
    except KeyboardInterrupt:
        print("user canceled.")
