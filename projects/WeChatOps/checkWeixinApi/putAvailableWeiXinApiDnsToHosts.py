#!/usr/bin/python
# encoding: utf-8
# -*- coding: utf8 -*-
"""
Created by PyCharm.
File:               LinuxBashShellScriptForOps:putAvailableWeiXinApiDnsToHosts.py
User:               Guodong
Create Date:        2017/1/19
Create Time:        9:33
 """


# TODO(Guodong Ding) write a validator decorator fot parameters type and format
def dns_query(domain):
    import dns.resolver

    domain = domain or "api.weixin.qq.com"

    query = dns.resolver.Resolver()
    query.nameservers = ['114.114.114.114']
    query.timeout = 1.0
    query.lifetime = 3.0
    return query.query(domain, 'A').response.answer


def query_httpdns():
    pass


print(dns_query("qyapi.weixin.qq.com"))
print(dns_query("qy.weixin.qq.com"))
