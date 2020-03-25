#!/usr/bin/python
# encoding: utf-8
# -*- coding: utf8 -*-
import dns.resolver

domain = "api.weixin.qq.com"

query = dns.resolver.Resolver()
query.nameservers = ['14.114.114.114']
query.timeout = 1.0
query.lifetime = 3.0  # dns.exception.Timeout: The DNS operation timed out after 3.0 seconds
answer = query.query(domain, 'A').response.answer  # type: [dns.rrset.RRset,]

for record in answer[-1]:
    print "A records: %s" % record


def get_ip_with_socket(hostname):
    import socket
    try:
        ip_address = socket.gethostbyname_ex(hostname)[-1]
    except socket.error:
        return None
    return ip_address


print(get_ip_with_socket(domain))
