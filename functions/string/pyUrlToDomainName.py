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
Long Description:       
References:             https://stackoverflow.com/questions/9626535/get-domain-name-from-url
                        https://ashiknesin.com/blog/get-domain-name-url-string-python/
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


def get_domain_name_from_url(url):
    # https://stackoverflow.com/questions/9626535/get-domain-name-from-url
    # https: // docs.python.org / 2 / library / urlparse.html
    from urlparse import urlparse
    parsed_uri = urlparse(url)
    # domain = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)
    domain_name = "{uri.netloc}".format(uri=parsed_uri)
    return domain_name


def get_domain_name_from_url_alternative_method_1(url):
    # https://ashiknesin.com/blog/get-domain-name-url-string-python/
    import tldextract
    extract_result = tldextract.extract(url)
    domain_name = extract_result.subdomain + '.' + extract_result.domain + '.' + extract_result.suffix
    return domain_name


if __name__ == '__main__':
    url_to_test = 'http://xinbao.osap-saas.com/wss/OSAP'
    print get_domain_name_from_url(url_to_test)
    print get_domain_name_from_url_alternative_method_1(url_to_test)
