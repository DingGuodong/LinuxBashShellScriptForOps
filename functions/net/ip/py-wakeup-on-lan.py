#!/usr/bin/python
# encoding: utf-8
# -*- coding: utf-8 -*-
"""
Created by PyCharm.
File Name:              LinuxBashShellScriptForOps:py-wakeup-on-lan.py
Version:                0.0.1
Author:                 Guodong
Author Email:           dgdenterprise@gmail.com
URL:                    https://github.com/DingGuodong/LinuxBashShellScriptForOps
Download URL:           https://github.com/DingGuodong/LinuxBashShellScriptForOps/tarball/master
Create Date:            2018/10/23
Create Time:            11:59
Description:            wake on lan, WoL
Long Description:       
References:             
Prerequisites:          pip install wakeonlan
Development Status:     3 - Alpha, 5 - Production/Stable
Environment:            Console
Intended Audience:      System Administrators, Developers, End Users/Desktop
License:                Freeware, Freely Distributable
Natural Language:       English, Chinese (Simplified)
Operating System:       POSIX :: Linux, Microsoft :: Windows
Programming Language:   Python :: 3
Topic:                  Utilities
 """
from wakeonlan import send_magic_packet

mac_lan = '34-E6-D7-4A-E6-0F'
mac_wlan = '3c:a9:f4:bd:70:00'
# test PASSED on Dell Latitude E6440. 192.168.88.255 is broadcast address of LAN
send_magic_packet(mac_lan, ip_address='192.168.88.255')

# test FAILED when using Wake on WLAN on Dell Latitude E6440.
send_magic_packet(mac_wlan, ip_address='192.168.88.255')
