#!/usr/bin/python
# encoding: utf-8
# -*- coding: utf8 -*-
"""
Created by PyCharm.
File:               LinuxBashShellScriptForOps:getPublicIPAddress_urllib2Impl
User:               Guodong
Create Date:        2016/7/27
Create Time:        16:59

pip install urllib3 certifi
or
pip install urllib3[secure]

 """
import certifi
import urllib3

# http://icanhazip.com/
# http://ipecho.net/plain
# https://ifconfig.co/

api_url = "https://ifconfig.co/"
api_country = "https://ifconfig.co/country"
api_city = "https://ifconfig.co/city"


class GetIP(object):
    def __init__(self):
        self.api_url = api_url
        self.api_country = api_country
        self.api_city = api_city
        self.http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED', ca_certs=certifi.where())

    def json(self):
        req = self.http.request('GET', self.api_url, headers={'Accept': 'application/json'})
        if req.status == 200:
            return req.data

    def country(self):
        req = self.http.request('GET', self.api_country, headers={'Accept': 'application/json'})
        if req.status == 200:
            return req.data

    def city(self):
        req = self.http.request('GET', self.api_city, headers={'Accept': 'application/json'})
        if req.status == 200:
            return req.data


if __name__ == '__main__':
    c = GetIP()
    # print(c.country())
    # print(c.city())
    print(c.json())
