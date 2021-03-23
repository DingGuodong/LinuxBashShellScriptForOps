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
import datetime
import pprint
import socket
import ssl
import time

try:
    from socket import errorTab
except ImportError:
    errorTab = {
        10004: 'The operation was interrupted.',
        10009: 'A bad file handle was passed.',
        10013: 'Permission denied.',
        10014: 'A fault occurred on the network??',
        10022: 'An invalid operation was attempted.',
        10035: 'The socket operation would block',
        10036: 'A blocking operation is already in progress.',
        10048: 'The network address is in use.',
        10054: 'The connection has been reset.',
        10058: 'The network has been shut down.',
        10060: 'The operation timed out.',
        10061: 'Connection refused.',
        10063: 'The name is too long.',
        10064: 'The host is down.',
        10065: 'The host is unreachable.'
    }

# soc = ssl.SSLSocket(socket.socket(),
#                     ca_certs=certifi.where(),
#                     cert_reqs=ssl.CERT_REQUIRED)
soc = ssl.wrap_socket(socket.socket(), ca_certs=certifi.where(), cert_reqs=ssl.CERT_REQUIRED)  # type: ssl.SSLSocket
try:
    soc.connect(("github.com", 443))
except socket.error as e:
    # such as '10061', '[Errno 10061]  Connection refused.'
    print(str(e), errorTab.get(int(str(e).strip()[7:-1])))

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
