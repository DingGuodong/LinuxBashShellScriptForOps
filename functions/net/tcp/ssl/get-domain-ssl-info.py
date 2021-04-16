#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created by PyCharm.
File Name:              LinuxBashShellScriptForOps:get-domain-ssl-info.py
Version:                0.0.1
Author:                 dgden
Author Email:           dgdenterprise@gmail.com
URL:                    https://github.com/DingGuodong/LinuxBashShellScriptForOps
Download URL:           https://github.com/DingGuodong/LinuxBashShellScriptForOps/tarball/master
Create Date:            2021/4/14
Create Time:            11:27
Description:            get the certificate's issuer and the valid days count
Long Description:       
References:             
Prerequisites:          []
                        Internet access maybe is required
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
import datetime
import socket
import ssl
import sys

import certifi


def get_cert_info(hostname):
    ssl_context = ssl.create_default_context(cafile=certifi.where())
    ssl_conn = ssl_context.wrap_socket(
        socket.socket(socket.AF_INET),
        server_hostname=hostname,
    )

    ssl_conn.settimeout(30.0)

    max_tries = 3
    tried_time = 0
    while True:
        try:
            ssl_conn.connect((hostname, 443))
            break
        except socket.error as e:
            tried_time += 1
            # such as 'socket.error: [Errno 10060]'
            print(e, "try again, ({}/{})".format(max_tries, tried_time))
            if tried_time == max_tries:
                print("Exceed max number of try times, {}".format(max_tries))
                sys.exit(1)

    cert_info = ssl_conn.getpeercert()

    return cert_info


def get_cert_issuer(hostname):
    cert_info = get_cert_info(hostname)
    issuer = dict([tuple(x[0]) for x in cert_info.get('issuer')])
    common_name = issuer.get('commonName')
    return common_name


def get_cert_expiry_datetime(hostname):
    ssl_date_fmt = r'%b %d %H:%M:%S %Y %Z'
    cert_info = get_cert_info(hostname)
    # parse the string from the certificate into a Python datetime object
    return datetime.datetime.strptime(cert_info['notAfter'], ssl_date_fmt)


def get_cert_valid_days_remaining(hostname):
    """Get the number of days left in a cert's lifetime."""
    expires = get_cert_expiry_datetime(hostname)
    return (expires - datetime.datetime.utcnow()).days


def is_cert_expired_after_days(hostname, after_days=14):
    """Check if `hostname` SSL cert expires is within `after_days`.

    Raises `AlreadyExpired` if the cert is past due
    """
    days_remaining = get_cert_valid_days_remaining(hostname)

    # if the cert expires in less than two weeks, we should reissue it
    if days_remaining < datetime.timedelta(days=0).days:
        # cert has already expired - uhoh!
        raise Exception("Cert expired %s days ago" % days_remaining)
    elif days_remaining < datetime.timedelta(days=after_days).days:
        # expires sooner than the buffer
        return True
    else:
        # everything is fine
        return False


def show_domain_info(hostname):
    domain = hostname
    # is_ssl_enable = True
    remain_days = get_cert_valid_days_remaining(hostname)
    issuer = get_cert_issuer(hostname)
    print("Domain: {}, DaysLeft: {}, Issuer: {}".format(
        domain,
        remain_days,
        issuer
    ))


if __name__ == '__main__':
    show_domain_info("github.com")
