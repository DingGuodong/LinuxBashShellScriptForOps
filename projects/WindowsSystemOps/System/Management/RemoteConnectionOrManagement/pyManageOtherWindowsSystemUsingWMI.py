#!/usr/bin/python
# encoding: utf-8
# -*- coding: utf8 -*-
"""
Created by PyCharm.
File:               LinuxBashShellScriptForOps:pyManageOtherWindowsSystemUsingWMI.py
User:               Guodong
Create Date:        2017/9/20
Create Time:        11:01
Description:        
References:         https://pypi.python.org/pypi/WMI/
                    http://timgolden.me.uk/python/wmi/index.html
                    http://timgolden.me.uk/python/wmi/tutorial.html
                    http://timgolden.me.uk/python/wmi/cookbook.html
                    https://msdn.microsoft.com/en-us/library/aa394582(v=vs.85).aspx
                    https://msdn.microsoft.com/en-us/library/aa394572%28VS.85%29.aspx
                    https://msdn.microsoft.com/en-us/library/aa394554(v=vs.85).aspx
                    [Operating System Classes](https://msdn.microsoft.com/en-us/library/dn792258(v=vs.85).aspx)
                    [Win32_OperatingSystem class](https://msdn.microsoft.com/en-us/library/aa394239%28v=vs.85%29.aspx)
Prerequisites:      [wmi,]
 """
import wmi
import time
from collections import Iterable

host = "192.168.88.29"
username = "chris.ding@example.domain"
secret = "your password here"


def time_converter(string):
    # string is a datetime type got from WMI, format like '20170920151143.233000+480' and '20150902091441.000000+480'
    return time.strftime('%Y-%m-%d %H:%M:%S', time.strptime(string.split(".")[0], '%Y%m%d%H%M%S'))


def wmi_instance(computer, user, password):
    try:
        #
        # Using wmi module before 1.0rc3
        #
        connection = wmi.connect_server(server=computer, user=user, password=password)
        instance = wmi.WMI(wmi=connection)
        return instance
    except Exception as ex:
        del ex
        #
        # Using wmi module at least 1.0rc3
        #
        instance = wmi.WMI(computer=computer, user=user, password=password)
        return instance


print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))

c = None

try:
    c = wmi_instance(host, username, secret)
except Exception as e:
    print e
    if isinstance(e, Iterable):
        for msg in e:
            print msg
    for msg in e.args:
        print msg

    for msg in e.message:
        print msg

if c is not None:
    # [Win32_ComputerSystem class](https://msdn.microsoft.com/en-us/library/aa394102%28v=vs.85%29.aspx)
    for com in c.Win32_ComputerSystem():
        print
        print com.BootupState, com.Status
        print com.Caption
        print com.DNSHostName, com.Domain, com.DomainRole, com.PartOfDomain, com.Roles
        print com.Description, com.Manufacturer, com.Model, com.SystemType, com.OEMStringArray
        print com.NumberOfProcessors, com.NumberOfLogicalProcessors
        print com.TotalPhysicalMemory

    # get ip address on Windows with WMI python module
    wql_query_ip = "SELECT IPAddress FROM Win32_NetworkAdapterConfiguration WHERE IPEnabled = 'True'"
    for ip in c.query(wql_query_ip):
        print ip.IPAddress[0]

    # get some system information on Windows with WMI, such as hostname , version, arch and languages
    for os in c.Win32_OperatingSystem():
        # https://msdn.microsoft.com/en-us/library/aa387937%28v=vs.85%29.aspx
        print os.Caption.strip(), os.Version, os.OSArchitecture, os.MUILanguages
        print os.CSName
        print os.CountryCode, os.CurrentTimeZone / 60
        print time_converter(os.InstallDate)
        print time_converter(os.LastBootUpTime)

    # get disk usage with WMI
    for disk in c.Win32_LogicalDisk(DriveType=3):
        print disk.Caption, "%0.2f%% free" % (100.0 * long(disk.FreeSpace) / long(disk.Size))

    # get stopped service which should started
    stopped_services = c.Win32_Service(StartMode="Auto", State="Stopped")
    if stopped_services:
        for s in stopped_services:
            print s.Caption, "service is not running"
    else:
        print "No auto services stopped"

    # see what is printing in printer
    for printer in c.Win32_Printer():
        print printer.Caption
        for job in c.Win32_PrintJob(DriverName=printer.DriverName):
            print "  ", job.Document

    # see who is using printer
    print_job_watcher = c.Win32_PrintJob.watch_for(
        notification_type="Creation",
        delay_secs=1
    )
    while True:
        pj = print_job_watcher()
        print "User %s has submitted %d pages to printer %s" % \
              (pj.Owner, pj.TotalPages, pj.Name)
