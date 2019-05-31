#!/usr/bin/python
# encoding: utf-8
# -*- coding: utf8 -*-
"""
Created by PyCharm.
File:               LinuxBashShellScriptForOps:pyPingIcmpNetworkLatency.py
User:               Guodong
Create Date:        2016/11/30
Create Time:        9:19

# python pyPingIcmpNetworkLatency.py
ping 192.168.1.1 with ... get ping in 3.0000ms
ping 192.168.1.1 with ... get ping in 5.0001ms
ping 192.168.1.1 with ... get ping in 17.0000ms
ping 192.168.1.1 with ... get ping in 3.0000ms

 """

import os
import sys

try:
    import ping
except ImportError:
    try:
        command_to_execute = "pip install ping || easy_install ping"
        os.system(command_to_execute)
    except OSError:
        print("Can NOT install 'ping', Aborted!")
        sys.exit(1)
    except Exception as e:
        print("Uncaught exception, %s" % str(e))
        sys.exit(1)
    import ping

try:
    ping.verbose_ping("192.168.88.1")
except Exception as e:
    # Note that ICMP messages can only be sent from processes running as root.
    if "10013" in str(e) or "as root" in str(e):
        print("socket.SOCK_RAW require super administrator privilege")
    else:
        print(e.args)
    sys.exit(1)
