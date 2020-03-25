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
Description:            python query dns RR(Resource Records), such as A, NS, CNAME, MX, TXT, SRV, etc
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
Tips:                   [PEP 484 -- Type Hints](https://www.python.org/dev/peps/pep-0484/)
                        [PEP 483 -- The Theory of Type Hints](https://www.python.org/dev/peps/pep-0483/)
                        [Type hints cheat sheet (Python 2)](https://mypy.readthedocs.io/en/latest/cheat_sheet.html)
 """
import dns.resolver


def query_dns_rr(qname, rdtype=dns.rdatatype.A, nameserver="8.8.8.8", debug=False):
    # type: (str, str, str, bool) -> list
    """
    query ip address of given domain name
    :param qname: domain name
    :param rdtype: A, CNAME, MX, TXT, NS, SRV, ...
    :param nameserver:
    :param debug: enable debug,
    :return: list
    """
    if 'http' in qname:
        qname = get_domain_name_from_url(qname)

    if isinstance(rdtype, basestring):
        rdtype = dns.rdatatype.from_text(rdtype)

    resolver = dns.resolver.Resolver()
    resolver.timeout = 3  # TODO(Guodong) does it really works?
    resolver.lifetime = 3.0  # dns.exception.Timeout: The DNS operation timed out after 3.0 seconds
    resolver.nameservers = [nameserver]  # default_nameserver = resolver.nameservers
    resolver.cache = False
    answer = None
    try:
        answer = resolver.query(qname, rdtype).response.answer  # type: [dns.rrset.RRset,]
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
    answers = []
    if answer:
        for record in answer:
            records.append(record)  # redefined __str__ in <class 'dns.rrset.RRset'>

    for items in records:  # same as answer[-1].__str__()
        if items.rdtype == rdtype:
            for item in items:  # same as 'item.items', redefined __iter__ and __len__ in  <class 'dns.Set'>
                answers.append(str(item))

    return answers


def get_domain_name_from_url(url):
    # type: (str) -> str
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
    # support to resolve domain name in Chinese
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

    print(query_dns_rr("github.com", rdtype="A", nameserver="114.114.114.114"))
    print(query_dns_rr("www.jd.com", rdtype="CNAME", nameserver="114.114.114.114"))
    print(query_dns_rr("github.com", rdtype="NS", nameserver="114.114.114.114"))
    print(query_dns_rr("github.com", rdtype="MX", nameserver="114.114.114.114"))
    print(query_dns_rr("aliyun.com", rdtype="TXT", nameserver="114.114.114.114"))
