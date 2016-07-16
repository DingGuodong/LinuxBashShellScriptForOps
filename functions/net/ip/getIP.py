#!/usr/bin/python
# encoding: utf-8
# -*- coding: utf8 -*-

import socket


class GetIP(object):
    def __init__(self, ip_type):
        self.ip = None
        self.ip_type = ip_type

    @staticmethod
    def get_all_ip():
        ip_lists = socket.gethostbyname_ex(socket.gethostname())
        for ip_list in ip_lists:
            if isinstance(ip_list, list):
                if ip_lists[0] is not None:
                    local_ips = ip_list
        return local_ips

    @staticmethod
    def get_local_ip():
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            s.connect(("www.aliyun.com", 80))
        except StandardError:
            return None
        else:
            return s.getsockname()[0]

    def get(self):
        if self.ip_type == "local":
            return self.get_local_ip()
        elif self.ip_type == "all":
            return self.get_all_ip()
        else:
            return None


ips = GetIP("all")
print ips.get()

ipa = GetIP("local")
print ipa.get()
