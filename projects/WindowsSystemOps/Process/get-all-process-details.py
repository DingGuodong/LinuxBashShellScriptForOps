#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created by PyCharm.
File Name:              LinuxBashShellScriptForOps:get-all-process-details.py
Version:                0.0.1
Author:                 dgden
Author Email:           dgdenterprise@gmail.com
URL:                    https://github.com/DingGuodong/LinuxBashShellScriptForOps
Download URL:           https://github.com/DingGuodong/LinuxBashShellScriptForOps/tarball/master
Create Date:            2020/2/7
Create Time:            14:13
Description:            
Long Description:       
References:             Best way to continuously write and read data to file/local database
                        InfluxDB
                        [InfluxDB](https://www.influxdata.com/get-influxdb/)

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
from collections import OrderedDict

import psutil

for proc in psutil.process_iter():
    try:
        # print(dir(proc))
        name = proc.name()
        exe = proc.exe()
        cpu_percent = proc.cpu_percent(0.1)
        cpu_user = proc.cpu_times().user
        cpu_system = proc.cpu_times().system
        cmdline = " ".join(proc.cmdline()) if len(proc.cmdline()) > 0 else ""

        # proc.dict = proc.as_dict(
        #     ["name", "exe", "cpu_percent", "cpu_times",  "cmdline"]
        # )
        # print(proc.dict)
        result = OrderedDict()
        result["name"] = name
        result["exe"] = exe
        result["cpu_percent"] = cpu_percent
        result["cpu_user"] = cpu_user
        result["cpu_system"] = cpu_system
        result["cmdline"] = cmdline
        print("|".join([str(v) for v in result.values()]))

    except psutil.AccessDenied:
        pass
