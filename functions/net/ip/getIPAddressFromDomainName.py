#!/usr/bin/python
# encoding: utf-8
# -*- coding: utf8 -*-
"""
Created by PyCharm.
File Name:              LinuxBashShellScriptForOps:getIPAddressFromDomainName.py
Version:                0.0.1
Author:                 Guodong
Author Email:           dgdenterprise@gmail.com
URL:                    https://github.com/DingGuodong/LinuxBashShellScriptForOps
Download URL:           https://github.com/DingGuodong/LinuxBashShellScriptForOps/tarball/master
Create Date:            2017/10/31
Create Time:            11:13
Description:            Python get IP address from domain name(URL)
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


def get_domain_name_from_url(url):
    # https://stackoverflow.com/questions/9626535/get-domain-name-from-url
    # https: // docs.python.org / 2 / library / urlparse.html
    if not is_url_valid(url):
        raise RuntimeError("invalid URL.")
    from urlparse import urlparse
    parsed_uri = urlparse(url)
    # domain = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)
    domain_name = "{uri.netloc}".format(uri=parsed_uri)
    if ":" in domain_name:
        return domain_name.strip().split(":")[0]
    else:
        return domain_name


def get_ip_address_from_domain_name(domain):
    import socket
    result = ""
    try:
        result = socket.gethostbyname(domain)
    except socket.gaierror:
        pass
    return result


def is_url_valid(url):
    # http://stackoverflow.com/questions/7160737/python-how-to-validate-a-url-in-python-malformed-or-not
    from django.core.validators import URLValidator
    from django.core.exceptions import ValidationError
    val = URLValidator()
    try:
        val(url)
    except ValidationError:
        return False
    else:
        return True


def is_url_valid_am1(url):  # 'am' is short for 'alternative method'
    """
    http://validators.readthedocs.io/en/latest/
    Python has all kinds of validation tools, but every one of them requires defining a schema. I
    wanted to create a simple validation library where validating a simple value does not require
    defining a form or a schema.
    """
    import validators
    if validators.url(url):
        return True
    else:
        return False


if __name__ == '__main__':
    url_list = """
http://subdomain.domain/
"""
    for url_to_handle in url_list.strip().split('\n'):
        domain_name_middle = get_domain_name_from_url(url_to_handle)
        print get_ip_address_from_domain_name(domain_name_middle)
