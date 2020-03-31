#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created by PyCharm.
File Name:              LinuxBashShellScriptForOps:read-winevt.py
Version:                0.0.1
Author:                 dgden
Author Email:           dgdenterprise@gmail.com
URL:                    https://github.com/DingGuodong/LinuxBashShellScriptForOps
Download URL:           https://github.com/DingGuodong/LinuxBashShellScriptForOps/tarball/master
Create Date:            2020/3/30
Create Time:            15:53
Description:            get Windows Event Log
Long Description:
References:             https://serverfault.com/questions/743575/how-to-find-out-who-deleted-event-viewer-logs
                        https://docs.microsoft.com/en-us/powershell/module/microsoft.powershell.management/get-eventlog?view=powershell-5.1
                        https://stackoverflow.com/questions/11219213/read-specific-windows-event-log-event
                        https://www.accadius.com/using-python-read-windows-event-logs-multiple-servers/
                        https://www.accadius.com/wp-content/uploads/2017/07/MonitorEventLogs.py
Prerequisites:          pip install python-evtx
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

import contextlib
import mmap

import Evtx.Evtx as evtx
import datetime
import win32evtlog
import win32evtlogutil
import win32security
from Evtx.Views import evtx_file_xml_view
from lxml import etree

system_evt = r"C:\Windows\System32\winevt\Logs\System.evtx"


def get_evt_buff(path):
    with open(path, 'rb') as f:
        with contextlib.closing(mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)) as buf:
            yield buf


def to_lxml(record_xml):
    return etree.fromstring("<?xml version=\"1.0\" encoding=\"utf-8\" standalone=\"yes\" ?>%s" %
                            record_xml)


def get_child(node, tag, ns="{http://schemas.microsoft.com/win/2004/08/events/event}"):
    return node.find("%s%s" % (ns, tag))


def get_xml_info():
    for evt_buff in get_evt_buff(system_evt):
        fh = evtx.FileHeader(evt_buff, 0x0)

        for record_str, record in evtx_file_xml_view(fh):
            print record_str
            system = get_child(to_lxml(record_str.decode("gbk").encode("utf-8")), 'System')

            print get_child(system, 'EventID').text
            break


def is_datetime_newer(l_date, r_date, date_format):
    return datetime.datetime.strptime(l_date, date_format) > datetime.datetime.strptime(r_date, date_format)


def is_common_event_id(event_id):
    from itertools import chain
    common_event = {
        'Windows-Update-Failure': [20, 24, 25, 31, 34, 35],
        'Microsoft-Windows-Eventlog': [104, 1102],
        'Microsoft-Windows-TaskScheduler': [106],
        'Microsoft-Windows-DNS-Client': [1014],
        'Firewall-Rule-Add/Change/Delete': [2004, 2005, 2006, 2033],
        'Microsoft-Windows-Windows Defender': [3004],
        'Microsoft-Windows-Security-Auditing': [4720, 4724, 4725, 4728, 4732, 4635, 4740, 4748, 4756],
        'Service-Control-Manager': [7030, 7045],
        'App-Locker-Block/Warning': [03, 8004, 8006, 8007]
    }
    return event_id in chain(*common_event.values())


def get_event_log(server, log_type='system'):
    log_handle = win32evtlog.OpenEventLog(server, log_type)

    total_num_records = win32evtlog.GetNumberOfEventLogRecords(log_handle)

    flags = win32evtlog.EVENTLOG_BACKWARDS_READ | win32evtlog.EVENTLOG_SEQUENTIAL_READ

    print "There are %d records" % total_num_records
    events = 1
    while events:
        events = win32evtlog.ReadEventLog(log_handle, flags, 0)
        for event in events:
            if is_common_event_id(event.EventID):
                print event.EventID
                print event.EventCategory
                print event.TimeGenerated.Format()
                # print event.TimeWritten  # <type 'time'>
                print event.EventType  # win32evtlog.EVENTLOG_ERROR_TYPE,
                print event.ComputerName
                print event.SourceName
                print win32evtlogutil.SafeFormatMessage(event, log_type)  # Event Description
                # print event.StringInserts
                print event.Sid
                if event.Sid is not None:
                    try:
                        domain, user, typ = win32security.LookupAccountSid(server, event.Sid)
                        sidDesc = "%s/%s" % (domain, user)
                    except win32security.error:  # from pywintypes import error
                        sidDesc = str(event.Sid)
                    user_desc = "Event associated with user %s" % (sidDesc,)
                else:
                    user_desc = None
                print user_desc

    win32evtlog.CloseEventLog(log_handle)


if __name__ == '__main__':
    get_event_log('localhost', 'system')
