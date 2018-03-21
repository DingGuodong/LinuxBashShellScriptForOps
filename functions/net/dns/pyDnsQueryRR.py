#!/usr/bin/python
# encoding: utf-8
# -*- coding: utf8 -*-
"""
Created by PyCharm.
File Name:              LinuxBashShellScriptForOps:pyDnsQueryRR.py
Version:                0.0.1
Author:                 Guodong
Author Email:           dgdenterprise@gmail.com
URL:                    https://github.com/DingGuodong/LinuxBashShellScriptForOps
Download URL:           https://github.com/DingGuodong/LinuxBashShellScriptForOps/tarball/master
Create Date:            2018/3/21
Create Time:            11:11
Description:            python query dns RR(Resource Records)
Long Description:       
References:             
Prerequisites:          pip install dnspython
Development Status:     3 - Alpha, 5 - Production/Stable
Environment:            Console
Intended Audience:      System Administrators, Developers, End Users/Desktop
License:                Freeware, Freely Distributable
Natural Language:       English, Chinese (Simplified)
Operating System:       POSIX :: Linux, Microsoft :: Windows
Programming Language:   Python :: 2.6
Programming Language:   Python :: 2.7
Topic:                  Utilities
 """
import dns.resolver


def query_dns_rr(qname, rdtype="A", nameserver="8.8.8.8", debug=False):
    resolver = dns.resolver.Resolver()
    resolver.nameservers = [nameserver]  # default_nameserver = resolver.nameservers
    resolver.cache = False
    answer = None
    try:
        answer = resolver.query(qname, rdtype).response.answer
    except dns.resolver.NoAnswer as e:
        if debug:
            print(e)
        pass
    except dns.resolver.NXDOMAIN as e:
        if debug:
            print(e)
        pass
    except dns.exception.Timeout as e:
        if debug:
            print(e)
        pass
    except dns.resolver.NoNameservers as e:
        if debug:
            print(e)
        pass

    records = []
    if answer:
        for record in answer[-1]:
            records.append(str(record))
        return records
    else:
        return records


if __name__ == '__main__':
    query_list = [
        'www.baidu.com',
        'api.weixin.qq.com',
    ]

    for name in query_list:
        print(query_dns_rr(name, nameserver="114.114.114.114"))
