#!/usr/bin/python
# encoding: utf-8
# -*- coding: utf8 -*-
import dns.resolver

domain = "api.weixin.qq.com"

query = dns.resolver.Resolver()
query.nameservers = ['114.114.114.114']
query.timeout = 1.0
query.lifetime = 3.0
answer = query.query(domain, 'A').response.answer

# for record in answer[:-1]:
#     if len(record) <= 1:
#         print "CNAME records: %s" % record
#     else:
#         for cname in record:
#             print "CNAME records: %s" % cname

for record in answer[-1]:
    print "A records: %s" % record
