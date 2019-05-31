#!/usr/bin/python
# encoding: utf-8
# -*- coding: utf8 -*-
"""
Created by PyCharm.
File Name:              LinuxBashShellScriptForOps:pyGetSystemInformationWithWMI.py
Version:                0.0.1
Author:                 Guodong
Author Email:           dgdenterprise@gmail.com
URL:                    https://github.com/DingGuodong/LinuxBashShellScriptForOps
Download URL:           https://github.com/DingGuodong/LinuxBashShellScriptForOps/tarball/master
Create Date:            2017/12/5
Create Time:            20:08
Description:            get some system information by WMI with Python
Long Description:       Not recommend to use it if you not familiar WMI, can NOT trace
References:             https://pypi.python.org/pypi/WMI/1.4.9
                        http://timgolden.me.uk/python/wmi/index.html
                        http://timgolden.me.uk/python/wmi/tutorial.html
                        [wmi Cookbook](http://timgolden.me.uk/python/wmi/cookbook.html)
                        [Windows Management Instrumentation](https://msdn.microsoft.com/en-us/library/aa394582(v=vs.85).aspx)
                        [WMI Classes](https://msdn.microsoft.com/en-us/library/aa394554(v=vs.85).aspx)
                        [Operating System Classes](https://msdn.microsoft.com/en-us/library/dn792258(v=vs.85).aspx)
                        [Win32_OperatingSystem class](https://msdn.microsoft.com/en-us/library/aa394239%28v=vs.85%29.aspx)
Prerequisites:          []
Development Status:     3 - Alpha, 5 - Production/Stable
Environment:            Console
Intended Audience:      System Administrators, Developers, End Users/Desktop
License:                Freeware, Freely Distributable
Natural Language:       English, Chinese (Simplified)
Operating System:       Microsoft :: Windows
Programming Language:   Python :: 3

Topic:                  Utilities
 """
import wmi


c = wmi.WMI()
# https://msdn.microsoft.com/en-us/library/aa394102(v=vs.85).aspx
print(c.Win32_ComputerSystem()[0].Name)
print(c.Win32_ComputerSystem()[0])

# https://msdn.microsoft.com/en-us/library/aa394239(v=vs.85).aspx
for o in c.Win32_OperatingSystem():
    print(o.CSName, o.Caption, o.BuildNumber, o.OSArchitecture, o.SerialNumber, o.Version)

# https://msdn.microsoft.com/en-us/library/aa394173(v=vs.85).aspx
DRIVE_TYPES = {
    0: "Unknown",
    1: "No Root Directory",
    2: "Removable Disk",
    3: "Local Disk",
    4: "Network Drive",
    5: "Compact Disc",
    6: "RAM Disk"
}
for disk in c.Win32_LogicalDisk():
    print(disk.Caption, DRIVE_TYPES[disk.DriveType], disk.Description, disk.ProviderName or "")

for disk in c.Win32_LogicalDisk(DriveType=3):
    print(disk.Caption, "%0.2f%% free" % (100.0 * int(disk.FreeSpace) / int(disk.Size)))

# https://msdn.microsoft.com/en-us/library/aa394464(v=vs.85).aspx
for s in c.Win32_StartupCommand():
    print("[%s] %s <%s>" % (s.Location, s.Caption, s.Command))

# https://msdn.microsoft.com/en-us/library/aa394372(v=vs.85).aspx
for process in c.Win32_Process(Name='python.exe'):
    print(process.ProcessId, process.Name, process.CommandLine)

# https://msdn.microsoft.com/en-us/library/aa394418(v=vs.85).aspx
stopped_services = c.Win32_Service(StartMode="Auto", State="Stopped")
if stopped_services:
    for s in stopped_services:
        print(s.Caption, "service is not running")
else:
    print("No auto services stopped")

# https://msdn.microsoft.com/en-us/library/aa394217(v=vs.85).aspx
for interface in c.Win32_NetworkAdapterConfiguration(IPEnabled=1):
    print(interface.Description, interface.MACAddress)
    for ip_address in interface.IPAddress:
        print(ip_address)
    print()

# https://msdn.microsoft.com/en-us/library/aa394077(v=vs.85).aspx
for CIM_BIOSElement in c.Win32_BIOS():
    print(CIM_BIOSElement)

# get full serial number for LENOVO laptop computer, Dell products(Computers, Servers) maybe use this as well
print(c.Win32_ComputerSystem()[0].Model)  # SMBIOS|Type 1|System Information|Product Name
print(c.Win32_BIOS()[0].SerialNumber)  # Assigned serial number of the software element.
