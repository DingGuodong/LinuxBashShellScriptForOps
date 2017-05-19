#!/usr/bin/python
# encoding: utf-8
# -*- coding: utf8 -*-
"""
Created by PyCharm.
File:               LinuxBashShellScriptForOps:getPublicIPAddress
User:               Guodong
Create Date:        2016/7/27
Create Time:        16:30
 """

import pycurl
import certifi

# http://icanhazip.com/
# http://ipecho.net/plain
# https://ifconfig.co/
# http://ip.taobao.com/service/getIpInfo.php?ip=113.200.54.58&qq-pf-to=pcqq.group

api_url = "https://ifconfig.co/"
api_country = "https://ifconfig.co/country"
api_city = "https://ifconfig.co/city"

api_taobao = "http://ip.taobao.com/service/getIpInfo.php?ip="


class GetIP(object):
    def __init__(self):
        self.api_url = api_url
        self.api_country = api_country
        self.api_city = api_city

    def cli(self):
        curl = pycurl.Curl()
        curl.setopt(pycurl.TIMEOUT, 10)
        curl.setopt(pycurl.URL, self.api_url)
        curl.setopt(pycurl.CAINFO, certifi.where())
        curl.setopt(pycurl.HTTPHEADER, ['User-Agent: curl/7.35.0', 'Content-Type: text/plain; charset=utf-8'])
        return curl.perform()

    def json(self):
        curl = pycurl.Curl()
        curl.setopt(pycurl.URL, self.api_url)
        curl.setopt(pycurl.CAINFO, certifi.where())
        curl.setopt(pycurl.HTTPHEADER, ['User-Agent: curl/7.35.0', 'Accept: application/json'])
        return curl.perform()

    def country(self):
        curl = pycurl.Curl()
        curl.setopt(pycurl.URL, self.api_country)
        curl.setopt(pycurl.CAINFO, certifi.where())
        curl.setopt(pycurl.HTTPHEADER, ['User-Agent: HTTPie/0.8.0'])
        return curl.perform()

    def city(self):
        curl = pycurl.Curl()
        curl.setopt(pycurl.URL, self.api_city)
        curl.setopt(pycurl.CAINFO, certifi.where())
        curl.setopt(pycurl.HTTPHEADER, ['User-Agent: HTTPie/0.8.0'])
        return curl.perform()


c = GetIP()
c.cli()
# c.json()
# c.country()
# c.city()
