#!/usr/bin/python
# encoding: utf-8
# -*- coding: utf8 -*-
"""
Created by PyCharm.
File:               LinuxBashShellScriptForOps:pyGetCertsInfo.py
User:               Guodong
Create Date:        2016/12/1
Create Time:        13:58
 """
import datetime
import time
from socket import socket

from OpenSSL.SSL import Connection, Context, SSLv3_METHOD, TLSv1_2_METHOD

host = 'www.baidu.com'

try:
    ssl_connection_setting = Context(SSLv3_METHOD)
except ValueError:
    ssl_connection_setting = Context(TLSv1_2_METHOD)
ssl_connection_setting.set_timeout(30)

s = socket()
s.connect((host, 443))
c = Connection(ssl_connection_setting, s)
c.set_connect_state()
c.do_handshake()
cert = c.get_peer_certificate()
print "Issuer: ", cert.get_issuer()
print "Subject: ", cert.get_subject().get_components()
subject_list = cert.get_subject().get_components()
print "Common Name:", dict(subject_list).get("CN")
print "notAfter(UTC time): ", cert.get_notAfter()
UTC_FORMAT = "%Y%m%d%H%M%SZ"
utc_to_local_offset = datetime.datetime.fromtimestamp(time.time()) - datetime.datetime.utcfromtimestamp(time.time())
utc_time = time.mktime(time.strptime(cert.get_notAfter(), UTC_FORMAT))
local_time = utc_time + utc_to_local_offset.seconds
print "notAfter(Local Time): ", datetime.datetime.fromtimestamp(local_time)
print "is_expired:", cert.has_expired()

c.shutdown()
s.close()
