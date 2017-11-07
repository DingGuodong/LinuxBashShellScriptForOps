#!/usr/bin/python
# encoding: utf-8
# -*- coding: utf8 -*-
"""
Created by PyCharm.
File Name:              LinuxBashShellScriptForOps:zabbix-monitor-nginx-stub-status.py
Version:                0.0.1
Author:                 Guodong
Author Email:           dgdenterprise@gmail.com
URL:                    https://github.com/DingGuodong/LinuxBashShellScriptForOps
Download URL:           https://github.com/DingGuodong/LinuxBashShellScriptForOps/tarball/master
Create Date:            2017/11/6
Create Time:            20:39
Description:            Python get nginx stub status data for Zabbix use
Long Description:       
References:             http://nginx.org/en/docs/http/ngx_http_stub_status_module.html#stub_status
                        http://tengine.taobao.org/document/http_stub_status.html
Prerequisites:          []
                        pip install --upgrade pip
                        pip install -U urllib3
                        pip install -U requests
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
import re
import sys


class ZabbixMonitorNginx(object):
    def __init__(self, url):
        self.url = url
        self.data = self.http_request()
        self.stub_status_tuple = self.get_numbers_from_string()
        self.stub_status_dict = self.get_stub_status_dict()

    def help(self):
        pass

    def http_request(self):
        import requests
        import urllib3
        urllib3.disable_warnings()
        headers = {
            'cache-control': "no-cache",
        }

        response = requests.request("GET", self.url, headers=headers)
        if response.status_code == 200:
            return response.text.encode('utf-8')
        else:
            return ""

    def get_numbers_from_string(self):
        string_to_number = self.data.replace("\n", "").strip()
        pattern = re.compile("Active connections: (\d+) server accepts handled requests request_time"
                             " (\d+) (\d+) (\d+) (\d+)Reading: (\d+) Writing: (\d+) Waiting: (\d+)")
        match = pattern.search(string_to_number)
        if match:
            return match.groups()
        else:
            return tuple([0 for _ in range(8)])

    def get_stub_status_dict(self):
        stub_status_dict = {
            "connections_active": self.get_connections_active(),
            "connections_accepts": self.get_connections_accepts(),
            "connections_handled": self.get_connections_handled(),
            "connections_requests": self.get_connections_requests(),
            "request_time": self.get_request_time(),
            "connections_reading": self.get_connections_reading(),
            "connections_writing": self.get_connections_writing(),
            "connections_waiting": self.get_connections_waiting(),
        }
        return stub_status_dict

    def get_connections_active(self):
        # The current number of active client connections including Waiting connections.
        return self.stub_status_tuple[0]

    def get_connections_accepts(self):
        # The total number of accepted client connections.
        return self.stub_status_tuple[1]

    def get_connections_handled(self):
        # The total number of handled connections. Generally, the parameter value is the same as accepts unless
        # some resource limits have been reached (for example,the worker_connections limit).
        return self.stub_status_tuple[2]

    def get_connections_requests(self):
        # The total number of client requests.
        return self.stub_status_tuple[3]

    def get_request_time(self):
        # http://tengine.taobao.org/document/http_stub_status.html
        # The total requests' response time, which is in millisecond, is also recorded in the Tengine.
        # So you can calculate the mean response time.
        return self.stub_status_tuple[4]

    def get_connections_reading(self):
        # The current number of connections where nginx is reading the request header.
        return self.stub_status_tuple[5]

    def get_connections_writing(self):
        # The current number of connections where nginx is writing the response back to the client.
        return self.stub_status_tuple[6]

    def get_connections_waiting(self):
        # The current number of idle client connections waiting for a request.
        return self.stub_status_tuple[7]


if __name__ == '__main__':
    url_to_request = u"https://api.e-bao.cn/nginx_basic_status"
    zmn = ZabbixMonitorNginx(url_to_request)
    if len(sys.argv) == 1:
        print zmn.data
        print zmn.stub_status_tuple
        print zmn.stub_status_dict
    elif len(sys.argv) == 2:
        print zmn.stub_status_dict.get(sys.argv[1], 0)
    else:
        raise RuntimeError("bad call")
