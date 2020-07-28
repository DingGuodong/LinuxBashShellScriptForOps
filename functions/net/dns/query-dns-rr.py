#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created by PyCharm.
File Name:              LinuxBashShellScriptForOps:query-dns-rr.py
Version:                0.0.1
Author:                 dgden
Author Email:           dgdenterprise@gmail.com
URL:                    https://github.com/DingGuodong/LinuxBashShellScriptForOps
Download URL:           https://github.com/DingGuodong/LinuxBashShellScriptForOps/tarball/master
Create Date:            2020/7/28
Create Time:            15:50
Description:            query dns rr record
Long Description:       
References:             
Prerequisites:          []
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


def query_dns_rr(qname, rdtype=dns.rdatatype.A, nameserver="114.114.114.114", debug=False):
    # type: (str, str, str, bool) -> list
    """
    query ip address of given domain name
    :param qname: domain name
    :param rdtype: A, CNAME, MX, TXT, NS, SRV, ...
    :param nameserver:
    :param debug: enable debug,
    :return: list
    """
    if isinstance(rdtype, str):
        rdtype = dns.rdatatype.from_text(rdtype)

    resolver = dns.resolver.Resolver()
    resolver.timeout = 5
    resolver.lifetime = 10.0  # dns.exception.Timeout: The DNS operation timed out after 10.0 seconds
    resolver.nameservers = [nameserver]  # default_nameserver = resolver.nameservers
    resolver.cache = False
    answer = None
    try:
        answer = resolver.query(qname, rdtype).response.answer  # type: [dns.rrset.RRset,]
    except dns.resolver.NoAnswer as e:
        if debug:
            print(e)
    except dns.resolver.NXDOMAIN as e:
        if debug:
            print(e)
    except dns.exception.Timeout as e:
        if debug:
            print(e)
    except dns.resolver.NoNameservers as e:
        if debug:
            print(e)

    records = []
    answers = []
    if answer:
        for record in answer:
            records.append(record)  # redefined __str__ in <class 'dns.rrset.RRset'>

    for items in records:  # same as answer[-1].__str__()
        if items.rdtype == rdtype:
            for item in items:  # same as 'item.items', redefined __iter__ and __len__ in  <class 'dns.Set'>
                answers.append(str(item))

    return answers
