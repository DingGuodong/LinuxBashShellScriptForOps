#!/usr/bin/python
# encoding: utf-8
# -*- coding: utf8 -*-
"""
Created by PyCharm.
File Name:              LinuxBashShellScriptForOps:pyManageServicesOnOtherWindowsSystem.py
Version:                0.0.1
Author:                 Guodong
Author Email:           dgdenterprise@gmail.com
URL:                    https://github.com/DingGuodong/LinuxBashShellScriptForOps
Download URL:           https://github.com/DingGuodong/LinuxBashShellScriptForOps/tarball/master
Create Date:            2017/11/30
Create Time:            10:00
Description:            using WMI control services on remote Windows system
Long Description:       
References:             [Win32_Service class](https://msdn.microsoft.com/en-us/library/aa394418(v=vs.85).aspx)
Prerequisites:          wmi
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


def always_to_utf8(text):
    import locale

    encoding = locale.getpreferredencoding()
    if isinstance(text, bytes):
        try:
            return text.decode(encoding)
        except UnicodeDecodeError:
            return text.decode("utf-8")

    else:
        return text  # do not need decode, return original object if type is not instance of string type
        # raise RuntimeError("expected type is str, but got {type} type".format(type=type(text)))



class remoteWindowsWMI(object):
    def __init__(self, server, user, password):
        self.server = server
        self.user = user
        self.password = password
        self.c = self.__connect()

    def __connect(self):
        connection = wmi.connect_server(server=self.server, user=self.user, password=self.password)
        instance = wmi.WMI(wmi=connection)
        return instance

    def getServiceStopped(self):
        service_stopped = list()
        for s in self.c.Win32_Service(StartMode="Auto", State="Stopped"):
            service_stopped.append(s.Name)
        return service_stopped

    def getServiceName(self, name):
        if isinstance(name, str):
            pass
        elif isinstance(name, str):
            name = always_to_utf8(name)
        for s in self.c.Win32_Service(Name=name):
            return s.Name, s.Caption, s.DisplayName

    def getServiceState(self, name):
        if isinstance(name, str):
            pass
        elif isinstance(name, str):
            name = always_to_utf8(name)
        for s in self.c.Win32_Service(Name=name):
            return s.State, s.Status

        for s in self.c.Win32_Service(DisplayName=name):
            return s.State, s.Status

        for s in self.c.Win32_Service():
            if name.lower() == s.Name.lower() or name.lower() == s.Caption.lower():
                return s.State, s.Status

    # more quick way
    def getServiceStatus(self, name):
        if isinstance(name, str):
            pass
        elif isinstance(name, str):
            name = always_to_utf8(name)
        for s in self.c.Win32_Service(Name=name):
            return s.State, s.Status

    def startServiceName(self, name):
        if isinstance(name, str):
            pass
        elif isinstance(name, str):
            name = always_to_utf8(name)
        for s in self.c.Win32_Service(StartMode="Auto", State="Stopped"):
            if name.lower() == s.Name.lower() or name.lower() == s.Caption.lower():
                s.StartService()
        self.getServiceState(name)

    def stopServiceName(self, name):
        if isinstance(name, str):
            pass
        elif isinstance(name, str):
            name = always_to_utf8(name)
        for s in self.c.Win32_Service(StartMode="Auto", State="Started"):
            if name.lower() == s.Name.lower() or name.lower() == s.Caption.lower():
                s.StopService()
        self.getServiceState(name)

    def restartServiceName(self, name):
        self.stopServiceName(name)
        self.startServiceName(name)
        self.getServiceState(name)


if __name__ == '__main__':
    o = remoteWindowsWMI("192.168.88.32", "Administrator@example.domian", "your password here")
    print(o.getServiceStopped())
    print(o.getServiceName('IsmServ'))
    print(o.getServiceState('IsmServ'))
