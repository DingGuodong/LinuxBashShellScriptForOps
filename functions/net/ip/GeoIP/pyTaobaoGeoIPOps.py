#!/usr/bin/python
# encoding: utf-8
# -*- coding: utf8 -*-
"""
Created by PyCharm.
File Name:              LinuxBashShellScriptForOps:pyTaobaoGeoIPOps.py
Version:                0.0.1
Author:                 Guodong
Author Email:           dgdenterprise@gmail.com
URL:                    https://github.com/DingGuodong/LinuxBashShellScriptForOps
Download URL:           https://github.com/DingGuodong/LinuxBashShellScriptForOps/tarball/master
Create Date:            2017/11/13
Create Time:            16:26
Description:            using Taobao IP Library to locate IP address
Long Description:       ip.taobao.com(web services) lets you discover information about a specific IP address free.
References:             http://ip.taobao.com/instructions.php
Prerequisites:          []
                        apt install python-pip
                        pip install --upgrade pip
                        pip install requests
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


class TaobaoGeoIP(object):
    def __init__(self, ip):
        self.__ip = ip
        self.__info = self.__getIPInfo()
        self.data = self.__parseJsonData()

    def __getIPInfo(self):
        import requests

        url = "http://ip.taobao.com/service/getIpInfo.php"

        querystring = {"ip": self.__ip}

        headers = {
            'cache-control': "no-cache",
        }

        response = requests.request("GET", url, headers=headers, params=querystring)

        if response.status_code == 200:
            return response.text

    def __parseJsonData(self):
        import json
        try:
            data_dict = json.loads(self.__info)
            return dict(data_dict)
        except ValueError as e:
            print e
            print e.args
            print e.message
            raise RuntimeError("fatal error: parse Json data failed")


if __name__ == '__main__':
    ip_to_search = "42.120.147.1"
    p = TaobaoGeoIP(ip_to_search)
    data = p.data["data"]
    if str(data["region_id"]).startswith("370"):  # 370 is located in Shandong Province
        pass
    else:
        # Action such as log it, send it into iptables input reject rules
        print "location of ip {ip} is invalid".format(ip=ip_to_search)
        print p.data
