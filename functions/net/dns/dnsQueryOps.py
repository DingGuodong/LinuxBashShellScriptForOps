#!/usr/bin/python
# encoding: utf-8
# -*- coding: utf8 -*-
import dns.resolver

domain = "www.baidu.com"

query = dns.resolver.Resolver()
query.nameservers = ['114.114.114.114']
query.timeout = 1.0
query.lifetime = 3.0
answer = query.query(domain, 'A').response.answer
for i in answer:
    for j in i:
        print j
