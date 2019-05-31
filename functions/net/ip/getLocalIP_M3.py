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
            command_to_execute = "pip3 install netifaces || easy_install3 netifaces"
            os.system(command_to_execute)
        except OSError:
            print("Can NOT install netifaces, Aborted!")
            print("""Microsoft Visual C++ Compiler for Python 2.7 maybe need installed or reinstalled.
See also: https://www.microsoft.com/en-us/download/confirmation.aspx?id=44266
It can be download here: \
https://download.microsoft.com/download/7/9/6/796EF2E4-801B-4FC4-AB28-B59FBF6D907B/VCForPython27.msi""")
            sys.exit(1)
        import netifaces

    routing_ip_address = '127.0.0.1'

    for interface in netifaces.interfaces():
        if interface == netifaces.gateways()['default'][netifaces.AF_INET][1]:
            try:
                routing_ip_address = netifaces.ifaddresses(interface)[netifaces.AF_INET][0]['addr']
            except KeyError:
                pass
    return routing_ip_address


if __name__ == '__main__':
    print(get_local_ip_address())
