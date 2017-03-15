#!/usr/bin/python
# encoding: utf-8
# -*- coding: utf8 -*-
"""
Created by PyCharm.
File:               LinuxBashShellScriptForOps:getLocalIP_M3.py
User:               Guodong
Create Date:        2017/3/15
Create Time:        16:29
 """


def get_local_ip_address():
    import os
    import sys

    try:
        import netifaces
    except ImportError:
        try:
            command_to_execute = "pip install netifaces || easy_install netifaces"
            os.system(command_to_execute)
        except OSError:
            print "Can NOT install netifaces, Aborted!"
            sys.exit(1)
        import netifaces

    routingIPAddr = '127.0.0.1'

    for interface in netifaces.interfaces():
        if interface == netifaces.gateways()['default'][netifaces.AF_INET][1]:
            try:
                routingIPAddr = netifaces.ifaddresses(interface)[netifaces.AF_INET][0]['addr']
            except KeyError:
                pass
    return routingIPAddr


if __name__ == '__main__':
    print get_local_ip_address()
