#!/usr/bin/python
# encoding: utf-8
# -*- coding: utf8 -*-
"""
Created by PyCharm.
File Name:              LinuxBashShellScriptForOps:validate_ip_or_domain_ACL.py
Version:                0.0.1
Author:                 Guodong
Author Email:           dgdenterprise@gmail.com
URL:                    https://github.com/DingGuodong/LinuxBashShellScriptForOps
Download URL:           https://github.com/DingGuodong/LinuxBashShellScriptForOps/tarball/master
Create Date:            2018/5/16
Create Time:            11:12
Description:            Validate if IP or Domain in ALLOWED_HOSTS
                        A list of strings representing the host/domain names that this Django site can serve.
                        This is a security measure to prevent HTTP Host header attacks,
                        which are possible even under many seemingly-safe web server configurations.
Long Description:       
References:             https://docs.djangoproject.com/en/2.0/ref/settings/#allowed-hosts
Prerequisites:          []
Development Status:     3 - Alpha, 5 - Production/Stable
Environment:            Console
Intended Audience:      System Administrators, Developers, End Users/Desktop
License:                Freeware, Freely Distributable
Natural Language:       English, Chinese (Simplified)
Operating System:       POSIX :: Linux, Microsoft :: Windows
Programming Language:   Python :: 3
Topic:                  Utilities
 """
import re


# Refer to django.http.request, django 1.11.9, 2.0
def split_domain_port(host):
    """
    Return a (domain, port) tuple from a given host.

    Returned domain is lower-cased. If the host is invalid, the domain will be
    empty.
    """
    host_validation_re = re.compile(r"^([a-z0-9.-]+|\[[a-f0-9]*:[a-f0-9.:]+\])(:\d+)?$")

    host = host.lower()

    if not host_validation_re.match(host):
        return '', ''

    if host[-1] == ']':
        # It's an IPv6 address without a port.
        return host, ''
    bits = host.rsplit(':', 1)
    domain, port = bits if len(bits) == 2 else (bits[0], '')
    # Remove a trailing dot (if present) from the domain.
    domain = domain[:-1] if domain.endswith('.') else domain
    return domain, port


# Refer to django.utils.http, django 1.11.9, 2.0
def is_same_domain(host, pattern):
    """
    Return ``True`` if the host is either an exact match or a match
    to the wildcard pattern.

    Any pattern beginning with a period matches a domain and all of its
    subdomains. (e.g. ``.example.com`` matches ``example.com`` and
    ``foo.example.com``). Anything else is an exact string match.
    """
    if not pattern:
        return False

    pattern = pattern.lower()

    # add ip range support
    if pattern.endswith("*") and host.split('.')[:-1:] == pattern.split('.')[:-1:]:
        return True

    return (
            pattern[0] == '.' and (host.endswith(pattern) or host == pattern[1:]) or
            pattern == host
    )


# Refer to django.http.request, django 1.11.9, 2.0
def validate_host(host, allowed_hosts):
    """
    Validate the given host for this site.

    Check that the host looks valid and matches a host or host pattern in the
    given list of ``allowed_hosts``. Any pattern beginning with a period
    matches a domain and all its subdomains (e.g. ``.example.com`` matches
    ``example.com`` and any subdomain), ``*`` matches anything, and anything
    else must match exactly.

    Note: This function assumes that the given host is lower-cased and has
    already had the port, if any, stripped off.

    Return ``True`` for a valid host, ``False`` otherwise.
    """
    for pattern in allowed_hosts:
        if pattern == '*' or is_same_domain(host, pattern):
            return True

    return False


if __name__ == '__main__':
    print(validate_host('localhost', ['localhost', '127.0.0.1', '[::1]']))
    print(validate_host('www.example.com', ['.example.com', '127.0.0.1', '[::1]']))
    print(validate_host('192.168.88.209', ['192.168.88.*', '127.0.0.1', '[::1]']))
