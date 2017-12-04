#!/usr/bin/python
# encoding: utf-8
# -*- coding: utf8 -*-
"""
Created by PyCharm.
File Name:              LinuxBashShellScriptForOps:pyServicesManagerBasedOnWMI.py
Version:                0.0.1
Author:                 Guodong
Author Email:           dgdenterprise@gmail.com
URL:                    https://github.com/DingGuodong/LinuxBashShellScriptForOps
Download URL:           https://github.com/DingGuodong/LinuxBashShellScriptForOps/tarball/master
Create Date:            2017/12/4
Create Time:            12:51
Description:            using WMI control services on local Windows system
Long Description:       
References:             https://sentry.io/for/python/
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

import wmi


def decoding(text):
    import sys
    import codecs
    import locale

    if isinstance(text, unicode):
        return text
    elif isinstance(text, (basestring, str)):
        pass
    else:
        return text  # do not need decode, return original object if type is not instance of string type
        # raise RuntimeError("expected type is str, but got {type} type".format(type=type(text)))

    mswindows = (sys.platform == "win32")

    try:
        encoding = locale.getdefaultlocale()[1] or ('ascii' if not mswindows else 'gbk')
        codecs.lookup(encoding)  # codecs.lookup('cp936').name == 'gbk'
    except Exception as _:
        del _
        encoding = 'ascii' if not mswindows else 'gbk'  # 'gbk' is Windows default encoding in Chinese language 'zh-CN'

    msg = text
    if mswindows:
        try:
            msg = text.decode(encoding)
            return msg
        except (UnicodeDecodeError, UnicodeEncodeError):
            pass
    return msg


def fn_timer(func):
    from functools import wraps

    @wraps(func)
    def function_timer(*args, **kwargs):
        if not enable_performance_statistics:
            return func(*args, **kwargs)
        else:
            import time
            time_begin = time.time()
            result = func(*args, **kwargs)
            time_end = time.time()
            print "Total time running {function_name}: {time_spent} seconds".format(function_name=func.func_name,
                                                                                    time_spent=(time_end - time_begin))
            return result

    return function_timer


class localWindowsWMI(object):
    def __init__(self):
        self.c = wmi.WMI()

    @fn_timer
    def getServiceStopped(self):
        service_stopped = list()
        for s in self.c.Win32_Service(StartMode="Auto", State="Stopped"):
            service_stopped.append(s.Name)
        return service_stopped

    @fn_timer
    def getServiceName(self, name):
        if isinstance(name, unicode):
            pass
        elif isinstance(name, (basestring, str)):
            name = decoding(name)
        win32_service_iterable = self.c.Win32_Service(Name=name)
        if len(win32_service_iterable) < 1:
            return None

        for s in win32_service_iterable:
            return s.Name, s.Caption, s.DisplayName

    @fn_timer
    def getServiceState(self, name):
        if isinstance(name, unicode):
            pass
        elif isinstance(name, (basestring, str)):
            name = decoding(name)
        for s in self.c.Win32_Service(Name=name):
            return s.State, s.Status

        for s in self.c.Win32_Service(DisplayName=name):
            return s.State, s.Status

        for s in self.c.Win32_Service():
            if name.lower() == s.Name.lower() or name.lower() == s.Caption.lower():
                return s.State, s.Status

    # more quick way
    @fn_timer
    def getServiceStatus(self, name):
        if isinstance(name, unicode):
            pass
        elif isinstance(name, (basestring, str)):
            name = decoding(name)
        for s in self.c.Win32_Service(Name=name):
            return s.State, s.Status

    @fn_timer
    def startServiceName(self, name):
        if isinstance(name, unicode):
            pass
        elif isinstance(name, (basestring, str)):
            name = decoding(name)
        for s in self.c.Win32_Service(StartMode="Auto", State="Stopped"):
            if name.lower() == s.Name.lower() or name.lower() == s.Caption.lower():
                s.StartService()
        self.getServiceState(name)

    @fn_timer
    def stopServiceName(self, name):
        if isinstance(name, unicode):
            pass
        elif isinstance(name, (basestring, str)):
            name = decoding(name)
        for s in self.c.Win32_Service(StartMode="Auto", State="Started"):
            if name.lower() == s.Name.lower() or name.lower() == s.Caption.lower():
                s.StopService()
        self.getServiceState(name)

    @fn_timer
    def restartServiceName(self, name):
        self.stopServiceName(name)
        self.startServiceName(name)
        self.getServiceState(name)


if __name__ == '__main__':
    enable_performance_statistics = False
    o = localWindowsWMI()
    print o.getServiceStopped()
    print o.getServiceName(u'ImControllerService')
    print o.getServiceState(u'ImControllerService')
    print o.getServiceStatus(u'ImControllerService')
