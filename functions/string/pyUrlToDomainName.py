#!/usr/bin/python
# encoding: utf-8
# -*- coding: utf8 -*-
"""
Created by PyCharm.
File Name:              LinuxBashShellScriptForOps:pyUrlToDomainName.py
Version:                0.0.1
Author:                 Guodong
Author Email:           dgdenterprise@gmail.com
URL:                    https://github.com/DingGuodong/LinuxBashShellScriptForOps
Download URL:           https://github.com/DingGuodong/LinuxBashShellScriptForOps/tarball/master
Create Date:            2017/10/31
Create Time:            11:17
Description:            URL Address to Domain Name, Python get domain name from URL
Long Description:       get protocol host name from url
References:             https://stackoverflow.com/questions/9626535/get-domain-name-from-url
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


def get_domain_name(url):
    # https://stackoverflow.com/questions/9626535/get-domain-name-from-url
    from urlparse import urlparse
    parsed_uri = urlparse(url)
    # domain = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)
    domain_name = "{uri.netloc}".format(uri=parsed_uri).split(":")[0]
    return domain_name


def get_domain_name_2(url):
    import urllib
    scheme, rest = urllib.splittype(url)
    host, rest = urllib.splithost(rest)
    return host.split(":")[0]


if __name__ == '__main__':
    url_to_test = 'https://www.gnu.org:443/software/bash/manual/bashref.html#Pipelines'
    print get_domain_name(url_to_test)  # most fast
    print get_domain_name_2(url_to_test)  # medium
