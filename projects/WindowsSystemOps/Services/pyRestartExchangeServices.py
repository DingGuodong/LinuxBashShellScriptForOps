#!/usr/bin/python
# encoding: utf-8
# -*- coding: utf8 -*-
"""
Created by PyCharm.
File Name:              LinuxBashShellScriptForOps:pyRestartExchangeServices.py
Version:                0.0.1
Author:                 Guodong
Author Email:           dgdenterprise@gmail.com
URL:                    https://github.com/DingGuodong/LinuxBashShellScriptForOps
Download URL:           https://github.com/DingGuodong/LinuxBashShellScriptForOps/tarball/master
Create Date:            2017/11/29
Create Time:            15:16
Description:            restart Exchange 2010 services with Python
Long Description:       sc stop MSExchangeImap4
                        ping -n 2 127.0.0.1>nul
                        sc start MSExchangeImap4
                        sc stop MSExchangeTransport
                        ping -n 2 127.0.0.1>nul
                        sc start MSExchangeTransport
References:             
Prerequisites:          []
Development Status:     3 - Alpha, 5 - Production/Stable
Environment:            Console
Intended Audience:      System Administrators, Developers, End Users/Desktop
License:                Freeware, Freely Distributable
Natural Language:       English, Chinese (Simplified)
Operating System:       Microsoft :: Windows
Programming Language:   Python :: 2.6
Programming Language:   Python :: 2.7
Topic:                  Utilities
 """
import sys
import time
import uuid
import win32service
from collections import Iterable

import win32serviceutil

UNKNOWN = 0
STOPPED = win32service.SERVICE_STOPPED or 1
START_PENDING = win32service.SERVICE_START_PENDING or 2
STOP_PENDING = win32service.SERVICE_STOP_PENDING or 3
RUNNING = win32service.SERVICE_RUNNING or 4

message_status_map = {
    UNKNOWN: "current service state is unknown.",
    STOPPED: "current service state is stopped.",
    START_PENDING: "current service state is start pending.",
    STOP_PENDING: "current service state is stop pending.",
    RUNNING: "current service state is running.",
}


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
        import time
        time_begin = time.time()
        result = func(*args, **kwargs)
        time_end = time.time()
        print "Total time running {function_name}: {time_spent} seconds".format(function_name=func.func_name,
                                                                                time_spent=(time_end - time_begin))

        return result

    return function_timer


def query_status(service_name='TermService'):
    status = win32serviceutil.QueryServiceStatus(service_name)[1]
    if status == RUNNING or status == START_PENDING:
        return True
    else:
        return False


@fn_timer
def start_service(service_name='TermService'):
    status = win32serviceutil.QueryServiceStatus(service_name)[1]
    if status == STOPPED:
        try:
            win32serviceutil.StartService(service_name)
        except Exception as _:
            del _
            print 'Access denied.'
            sys.exit(1)

        time.sleep(2)
        status = win32serviceutil.QueryServiceStatus(service_name)[1]
        if status == RUNNING:
            return True
        else:
            # blocking until service started
            running_flag = True
            try_times = 0
            sleep_seconds = 2
            waiting_time = 300
            while running_flag:
                print "waiting for service {service} restart.".format(service=service_name),
                status_code = win32serviceutil.QueryServiceStatus(service_name)[1]
                print message_status_map[status_code]
                if status_code == RUNNING:
                    running_flag = False
                time.sleep(sleep_seconds)
                try_times += 1
                if try_times > waiting_time / sleep_seconds:
                    send_message("FAILED: SERVICE CAN NOT RESTART", "CAN NOT RESTART SERVICE, TIMEOUT")
                    sys.exit(1)
            return True


@fn_timer
def restart_service(service_name='TermService'):
    current_uuid = uuid.uuid4().get_hex()
    print("INFO: RESTARTING SERVICE\'{service}\'".format(service=service_name) + current_uuid)
    send_message("INFO: RESTARTING SERVICE\'{service}\'".format(service=service_name),
                 "RESTARTING SERVICE.\n\n-------------------\n\n>ID: " + current_uuid)
    status = win32serviceutil.QueryServiceStatus(service_name)[1]
    if status == RUNNING:
        try:
            win32serviceutil.RestartService(service_name)
        except Exception as e:
            print 'Access denied or service not exist.'
            if isinstance(e.args, Iterable):
                for arg in e.args:
                    print decoding(arg),
            sys.exit(1)

        time.sleep(2)
        status = win32serviceutil.QueryServiceStatus(service_name)[1]
        if status == RUNNING:
            print("SUCCESS: SERVICE \'{service}\' RESTARTED".format(service=service_name) + current_uuid)
            send_message("SUCCESS: SERVICE \'{service}\' RESTARTED".format(service=service_name),
                         "SERVICE RESTARTED.\n\n-------------------\n\n>ID: " + current_uuid)
            return True
        else:
            # blocking until service started
            running_flag = True
            try_times = 0
            sleep_seconds = 2
            waiting_time = 300
            while running_flag:
                print "waiting for service {service} restart.".format(service=service_name)
                status_code = win32serviceutil.QueryServiceStatus(service_name)[1]
                if status_code == RUNNING:
                    running_flag = False
                time.sleep(sleep_seconds)
                try_times += 1
                if try_times > waiting_time / sleep_seconds:
                    print("FAILED: SERVICE  \'{service}\' CAN NOT START".format(service=service_name) + current_uuid)
                    send_message("FAILED: SERVICE  \'{service}\' CAN NOT START".format(service=service_name),
                                 "CAN NOT START SERVICE, TIMEOUT\n\n-------------------\n\n>ID: " + current_uuid)
                    sys.exit(1)

            print("SUCCESS: SERVICE \'{service}\' RESTARTED".format(service=service_name) + current_uuid)
            send_message("SUCCESS: SERVICE \'{service}\' RESTARTED".format(service=service_name),
                         "SERVICE RESTARTED.\n\n-------------------\n\n>ID: " + current_uuid)
            return True
    else:
        print message_status_map[status], " And this is unusual."
        print("WARNING: UNUSUAL SERVICE \'{service}\' STATE".format(service=service_name) + current_uuid)
        send_message("WARNING: UNUSUAL SERVICE \'{service}\' STATE".format(service=service_name),
                     "SERVICE STATE IS UNUSUAL.\n\n-------------------\n\n>ID: " + current_uuid)


def send_message(title=u'', message=u''):
    import json
    import requests
    access_token = "35c6fc4a5bf7916ab3e74ac497c0fcc0df57877940a7a1f0ebec1a150d7635b2"
    title = title or u"Test Message"
    content = message or u"Test message sent by Python over DingTalk"
    mobile = u'183xxxx1212'  # if there are more than one phone number to at, use space spilt them
    enable_at_all = False

    url = "https://oapi.dingtalk.com/robot/send"
    querystring = {"access_token": access_token}

    payload = {
        "msgtype": "markdown",
        "markdown": {
            "title": title,
            "text": "### {title}\n".format(title=title) +
                    content +
                    "\n"
        },
        "at": {
            "atMobiles": mobile.strip().split(" "),
            "isAtAll": enable_at_all
        }
    }

    headers = {
        'content-type': "application/json",
        'cache-control': "no-cache",
    }

    response = requests.request("POST", url, data=json.dumps(payload), headers=headers, params=querystring)

    result_string = response.text
    result_dict = json.loads(result_string)
    if result_dict["errcode"] == 0:
        print json.dumps(result_dict, indent=4)
    else:
        print json.dumps(result_dict, indent=4)


if __name__ == '__main__':
    services = {
        "exchange2010": {
            "version": "Version 14.3 ‎(Build 123.4)‎ ",
            "services": [
                "MSExchangeTransport",  # Microsoft Exchange 传输
                "MSExchangeImap4",  # Microsoft Exchange IMAP4
            ],
        }
    }
    for service in services['exchange2010']['services']:
        restart_service(service)
