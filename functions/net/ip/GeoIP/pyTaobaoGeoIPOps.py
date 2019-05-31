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
                        访问限制: 为了保障服务正常运行，每个用户的访问频率需小于1qps。

                        https://pythonhosted.org/python-geoip/
                        https://github.com/maxmind/GeoIP2-python
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
Programming Language:   Python :: 3
Topic:                  Utilities
 """

import json

import requests


class TaobaoGeoIP(object):
    def __init__(self, ip):
        self.__ip = str(ip)
        self.content = self.__get_text_from_api()  # raw json data in str obj from API upstream
        self.to_text = self.__parse_json_data  # return indented json data in str obj from API upstream
        self.to_dict = self.__parse_to_dict  # return dict obj from API upstream
        self.data = self.to_dict().get("data")  # dict obj from API upstream

    def __get_text_from_api(self):
        url = "http://ip.taobao.com/service/getIpInfo.php"

        querystring = {"ip": self.__ip}

        headers = {
            'cache-control': "no-cache",
        }

        response = requests.request("GET", url, headers=headers, params=querystring)

        if response.status_code == 200:
            return response.content

    def __parse_json_data(self):
        if self.content:
            try:
                data_dict = json.loads(self.content, encoding="utf-8")
                data_str = json.dumps(data_dict, ensure_ascii=False, indent=4)
                return data_str
            except ValueError as e:
                print(e)
                print(e.args)
                raise RuntimeError("fatal error: parse Json data failed")
        else:
            return None

    def __parse_to_dict(self):
        if self.content:
            try:
                data_dict = json.loads(self.content, encoding="utf-8")
                return data_dict
            except ValueError as e:
                print(e)
                print(e.args)
                raise RuntimeError("fatal error: parse Json data failed")
        else:
            return None

    def get_country_id(self):
        if self.data:
            return self.data.get("country_id")

    def get_country(self):
        if self.data:
            return self.data.get("country")

    def get_city(self):
        if self.data:
            return self.data.get("city")

    def get_isp(self):
        if self.data:
            return self.data.get("isp")


if __name__ == '__main__':
    ip_to_search = "42.120.147.1"
    p = TaobaoGeoIP(ip_to_search)
    print(p.get_country_id())
    print(p.get_country())
    print(p.get_city())
