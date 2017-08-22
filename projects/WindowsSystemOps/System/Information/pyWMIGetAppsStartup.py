#!/usr/bin/python
# encoding: utf-8
# -*- coding: utf8 -*-
"""
Created by PyCharm.
File:               LinuxBashShellScriptForOps:pyWMIGetAppsStartup.py
User:               Guodong
Create Date:        2017/8/22
Create Time:        20:14
Description:        What’s running on startup and from where?
References:         http://timgolden.me.uk/python/wmi/cookbook.html#what-s-running-on-startup-and-from-where
 """
import wmi

c = wmi.WMI()

for s in c.Win32_StartupCommand():
    print "[%s] %s <%s>" % (s.Location, s.Caption, s.Command)
