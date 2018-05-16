#!/usr/bin/python
# encoding: utf-8
# -*- coding: utf8 -*-
"""
Created by PyCharm.
File:               LinuxBashShellScriptForOps:validate_ip_address.py
User:               Guodong
Create Date:        2016/12/14
Create Time:        14:09

http://stackoverflow.com/questions/3462784/check-if-a-string-matches-an-ip-address-pattern-in-python
http://stackoverflow.com/questions/319279/how-to-validate-ip-address-in-python
 """
import os
import sys

try:
    from IPy import IP
except ImportError:
    try:
        command_to_execute = "pip install IPy || easy_install IPy"
        os.system(command_to_execute)
    except OSError:
        print "Can NOT install 'IPy', Aborted!"
        sys.exit(1)
    except Exception as e:
        print "Uncaught exception, %s" % e.message
        print "Import IPy failed!"
        sys.exit(1)
    from IPy import IP


def is_valid_ipv4(ip, version=4):
    try:
        result = IP(ip, ipversion=version)
    except ValueError:
        return False
    if result is not None and result != "":
        return True


def is_private_ipv4(ip, version=4):
    """
    check if the given ip address is valid and private ip
    :param ip:
    :param version:
    :return:
    """
    if is_valid_ipv4(ip, version):
        if IP(ip).iptype() == "PRIVATE":
            return True
        else:
            return False
    else:
        raise RuntimeError("Error: invalid ip address: %s" % ip)


if __name__ == '__main__':
    host = '192.168.88.209'
    if is_valid_ipv4(host):
        print(is_private_ipv4(host))
