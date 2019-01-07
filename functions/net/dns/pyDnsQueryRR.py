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
    if 'http' in qname:
        qname = get_domain_name_from_url(qname)

    resolver = dns.resolver.Resolver()
    resolver.timeout = 3  # TODO(Guodong) does it really works?
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


def get_domain_name_from_url(url):
    # https://stackoverflow.com/questions/9626535/get-domain-name-from-url
    # https://docs.python.org/2/library/urlparse.html
    from urlparse import urlparse
    parsed_uri = urlparse(url)
    # domain = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)
    domain_name = "{uri.netloc}".format(uri=parsed_uri)
    return domain_name


def to_unicode_or_bust(obj, encoding='utf-8'):
    # the function convert non-unicode object to unicode object
    if isinstance(obj, basestring):
        if not isinstance(obj, unicode):
            obj = unicode(obj, encoding)

    return obj


def unicode2punycode(obj):
    # support  to resolve domain name in Chinese
    if isinstance(obj, unicode):
        return obj.encode("idna")
    else:
        return obj


if __name__ == '__main__':
    query_list = [
        'www.baidu.com',
        'api.weixin.qq.com',
        "中国政府网.政务",  # 中国政府网中文域名
        'any_else_site_not_exists',
    ]

    for name in query_list:
        name = unicode2punycode(to_unicode_or_bust(name))
        print(query_dns_rr(name, nameserver="114.114.114.114"))
