#!/usr/bin/python
# encoding: utf-8
# -*- coding: utf8 -*-
"""
Created by PyCharm.
File:               LinuxBashShellScriptForOps:ipRelatedAllInAll.py
User:               Guodong
Create Date:        2017/3/6
Create Time:        11:01
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
    if is_valid_ipv4(ip, version):
        if IP(ip).iptype() == "PRIVATE":
            return True
        else:
            return False
    else:
        raise RuntimeError("Error: invalid ip address: %s" % ip)


def is_ip_in_subnet(ip, subnet):
    if "/" in ip:
        prefixlen = ip.split("/")[-1]
        ip = ip.split("/")[0]
        if prefixlen.isdigit():
            import IPy
            netmask = IPy.intToIp(IPy._prefixlenToNetmask(int(prefixlen), 4), 4)
        else:
            netmask = prefixlen
        ip = ip + "/" + netmask
    else:
        netmask = "255.255.255.255"
        ip = ip + "/" + netmask

    if "/" in subnet:
        prefixlen = subnet.split("/")[-1]
        subnet = subnet.split("/")[0]
        if prefixlen.isdigit():
            import IPy
            netmask = IPy.intToIp(IPy._prefixlenToNetmask(int(prefixlen), 4), 4)
        else:
            netmask = prefixlen
        subnet = subnet + "/" + netmask
    else:
        netmask = "255.255.255.255"
        subnet = subnet + "/" + netmask

    pass
