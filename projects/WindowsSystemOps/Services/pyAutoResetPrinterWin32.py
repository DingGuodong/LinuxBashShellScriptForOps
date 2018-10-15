#!/usr/bin/python
# encoding: utf-8
# -*- coding: utf-8 -*-
"""
Created by PyCharm.
File Name:              LinuxBashShellScriptForOps:pyAutoResetPrinterWin32.py
Version:                0.0.1
Author:                 Guodong
Author Email:           dgdenterprise@gmail.com
URL:                    https://github.com/DingGuodong/LinuxBashShellScriptForOps
Download URL:           https://github.com/DingGuodong/LinuxBashShellScriptForOps/tarball/master
Create Date:            2018/10/10
Create Time:            10:44
Description:            auto reset Spooler(Print Spooler) service when printer failure occurs
Long Description:       
References:             http://timgolden.me.uk/pywin32-docs/win32print.html
Prerequisites:          pypiwin32: pip install pypiwin32
                        Optional: install 'pywin32'
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

import os
import sys
import time
import win32print
import win32service

import win32serviceutil


def get_system_encoding():
    """
    The encoding of the default system locale but falls back to the given
    fallback encoding if the encoding is unsupported by python or could
    not be determined.  See tickets #10335 and #5846
    """
    import codecs
    import locale

    try:
        encoding = locale.getdefaultlocale()[1] or 'ascii'
        codecs.lookup(encoding)
    except Exception as _:
        del _
        encoding = 'ascii'
    return encoding


def reset_printer():
    """
    Note: administrator privilege is required

    this function do three things:
    1. stop Print Spooler service
    2. delete all job files
    3. start Print Spooler service
    :return:
    """
    service_name = 'spooler'.capitalize()
    win_dir = os.environ.get('windir', r'C:\Windows')
    printer_path = r"System32\spool\PRINTERS"
    path = os.path.join(win_dir, printer_path)

    status_code_map = {
        0: "UNKNOWN",
        1: "STOPPED",
        2: "START_PENDING",
        3: "STOP_PENDING",
        4: "RUNNING"
    }

    DEFAULT_LOCALE_ENCODING = get_system_encoding()

    print "printer spool folder is: %s" % path

    if os.path.exists(path):
        if os.listdir(path):
            print "reset printer spooler service in progress ..."

            status_code = win32serviceutil.QueryServiceStatus(service_name)[1]
            if status_code == win32service.SERVICE_RUNNING or status_code == win32service.SERVICE_START_PENDING:
                print "stopping service {service}".format(service=service_name)
                win32serviceutil.StopService(serviceName=service_name)

            # waiting for service stop, in case of WindowsError exception
            # 'WindowsError: [Error 32]' which means
            # 'The process cannot access the file because it is being used by another process'.
            running_flag = True
            while running_flag:
                print "waiting for service {service} stop.".format(service=service_name)
                status_code = win32serviceutil.QueryServiceStatus(service_name)[1]
                time.sleep(2)
                if status_code == win32service.SERVICE_STOPPED:
                    running_flag = False

            for top, dirs, nondirs in os.walk(path, followlinks=True):
                for item in nondirs:
                    path_to_remove = os.path.join(top, item)
                    try:
                        os.remove(path_to_remove)
                    except WindowsError:
                        time.sleep(2)
                        """ KNOWN ISSUE:
                        It will also can NOT remove some files in some Windows, such as 'Windows Server 2012'
                        Because file maybe used by a program named "Print Filter Pipeline Host",
                        "C:\Windows\System32\printfilterpipelinesvc.exe"
                        It will throw out  'WindowsError: [Error 32]' exception again.
                        """
                        os.remove(path_to_remove)
                    except Exception as e:
                        print e
                        print e.args
                        print e.message
                    print "file removed: {file}".format(file=path_to_remove)

            status_code = win32serviceutil.QueryServiceStatus(service_name)[1]
            if status_code != win32service.SERVICE_RUNNING and status_code != win32service.SERVICE_START_PENDING:
                print "starting service {service}".format(service=service_name)
                win32serviceutil.StartService(serviceName=service_name)
        else:
            print "current printer spooler in good state, skipped."
    else:
        print "Error: {path} not found, system files broken!".format(path=path)
        sys.exit(1)

    status_code = win32serviceutil.QueryServiceStatus(service_name)[1]
    if status_code == win32service.SERVICE_RUNNING or status_code == win32service.SERVICE_START_PENDING:
        print "[OK] reset printer spooler service successfully!"
    else:
        print "current service code is {code}, and service state is {state}.".format(code=status_code,
                                                                                     state=status_code_map[status_code])
        try:
            print "trying start spooler service..."
            win32serviceutil.StartService(serviceName=service_name)
            status_code = win32serviceutil.QueryServiceStatus(service_name)[1]
            if status_code == win32service.SERVICE_RUNNING or status_code == win32service.SERVICE_START_PENDING:
                print "service {service} started.".format(service=service_name)
        except Exception as e:
            print e
            print [msg.decode(DEFAULT_LOCALE_ENCODING) for msg in e.args]
            print e.message.decode(DEFAULT_LOCALE_ENCODING)


def printer_watchdog():
    DEFAULT_LOCALE_ENCODING = get_system_encoding()
    print win32print.EnumPrinters(win32print.PRINTER_ENUM_LOCAL)  # get local printers
    print win32print.EnumPrinters(win32print.PRINTER_ENUM_CONNECTIONS)  # get printers which other computer shared

    default_printer_name = win32print.GetDefaultPrinter()

    printer = win32print.OpenPrinter(default_printer_name)
    print win32print.GetPrinter(printer)

    jobs_list = list()
    total_seconds = 60 * 5
    sleep_seconds = 10
    times = total_seconds / sleep_seconds
    current_times = 0
    while True:
        jobs = win32print.EnumJobs(printer, 0, 3)
        if len(jobs) >= 1:
            for job in jobs:
                print job.get('pUserName'), job.get('Submitted'), job.get('pMachineName'), \
                    job.get('pDocument').decode(DEFAULT_LOCALE_ENCODING)
                jobs_list.append(job.get('JobId', -1))
            if jobs[0].get('JobId') in jobs_list or jobs[-1].get('JobId') in jobs_list:
                current_times += 1
            if current_times > times:
                print "printer need to be reset, ... "
                reset_printer()
                current_times = 0
        print 'looks good'
        time.sleep(sleep_seconds)


if __name__ == '__main__':
    printer_watchdog()
