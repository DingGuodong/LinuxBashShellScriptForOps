#!/usr/bin/python
# encoding: utf-8
# -*- coding: utf8 -*-
"""
Created by PyCharm.
File:               LinuxBashShellScriptForOps:pyCheckCerts.py
User:               Guodong
Create Date:        2016/12/1
Create Time:        11:37

SSL Server Test
performs a deep analysis of the configuration of any SSL web server on the public Internet.
https://globalsign.ssllabs.com/

 """
import certifi
import ssl
import pprint
import socket
import datetime
import time

soc = ssl.SSLSocket(socket.socket(),
                    ca_certs=certifi.where(),
                    cert_reqs=ssl.CERT_REQUIRED)
soc.connect(("www.baidu.com", 443))
cert = soc.getpeercert()
soc.close()

pprint.pprint(cert)
expire = cert['notAfter']
print "notAfter(UTC time): ", expire

GMT_FORMAT = '%b %d %H:%M:%S %Y GMT'
utc_to_local_offset = datetime.datetime.fromtimestamp(time.time()) - datetime.datetime.utcfromtimestamp(time.time())
now = datetime.datetime.now().strftime(GMT_FORMAT)

expire_timestamp = time.mktime(time.strptime(expire, GMT_FORMAT)) + utc_to_local_offset.seconds
print "notAfter(Local Time): ", datetime.datetime.fromtimestamp(expire_timestamp).strftime("%Y/%m/%d %H:%M:%S")
