#!/usr/bin/python
# encoding: utf-8
# -*- coding: utf8 -*-
"""
Created by PyCharm.
File:               LinuxBashShellScriptForOps:getNetworkStatus.py
User:               Guodong
Create Date:        2016/11/2
Create Time:        16:20

show Windows or Linux network Nic status, such as MAC address, Gateway, IP address, etc

# python getNetworkStatus.py
Routing Gateway:               10.6.28.254
Routing NIC Name:              eth0
Routing NIC MAC Address:       06:7f:12:00:00:15
Routing IP Address:            10.6.28.28
Routing IP Netmask:            255.255.255.0
 """
import os
import sys

try:
    import netifaces
except ImportError:
    try:
        command_to_execute = "pip install netifaces || easy_install netifaces"
        os.system(command_to_execute)
    except OSError:
        print("Can NOT install netifaces, Aborted!")
        sys.exit(1)
    import netifaces

routingGateway = netifaces.gateways()['default'][netifaces.AF_INET][0]
routingNicName = netifaces.gateways()['default'][netifaces.AF_INET][1]

for interface in netifaces.interfaces():
    if interface == routingNicName:
        # print netifaces.ifaddresses(interface)
        routingNicMacAddr = netifaces.ifaddresses(interface)[netifaces.AF_LINK][0]['addr']
        try:
            routingIPAddr = netifaces.ifaddresses(interface)[netifaces.AF_INET][0]['addr']
            # TODO(Guodong Ding) Note: On Windows, netmask maybe give a wrong result in 'netifaces' module.
            routingIPNetmask = netifaces.ifaddresses(interface)[netifaces.AF_INET][0]['netmask']
        except KeyError:
            pass

display_format = '%-30s %-20s'
print(display_format % ("Routing Gateway:", routingGateway))
print(display_format % ("Routing NIC Name:", routingNicName))
print(display_format % ("Routing NIC MAC Address:", routingNicMacAddr))
print(display_format % ("Routing IP Address:", routingIPAddr))
print(display_format % ("Routing IP Netmask:", routingIPNetmask))
