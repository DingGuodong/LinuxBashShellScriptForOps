#!/usr/bin/python
# encoding: utf-8
# -*- coding: utf8 -*-
"""
Created by PyCharm.
File:               LinuxBashShellScriptForOps:getPublicIPAddress_urllib2Impl
User:               Guodong
Create Date:        2016/7/27
Create Time:        16:59
 """

import urllib2

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

    def cli(self):
        req = urllib2.Request(self.api_url)
        req.add_header('User-Agent', 'curl/7.35.0')
        res = urllib2.urlopen(req)
        return res.read()

    def json(self):
        req = urllib2.Request(self.api_url)
        req.add_header('Accept', 'application/json')
        res = urllib2.urlopen(req)
        return res.read()

    def country(self):
        req = urllib2.Request(self.api_country)
        req.add_header('User-Agent', 'HTTPie/0.8.0')
        res = urllib2.urlopen(req)
        return res.read()

    def city(self):
        req = urllib2.Request(self.api_city)
        req.add_header('User-Agent', 'HTTPie/0.8.0')
        res = urllib2.urlopen(req)
        return res.read()


c = GetIP()
# print c.cli()
# print c.json()
# print c.country()
print c.city()
