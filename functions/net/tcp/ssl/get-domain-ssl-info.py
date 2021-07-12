#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Created by PyCharm.
File Name:              LinuxBashShellScriptForOps:get-domain-ssl-info.py
Version:                0.0.1
Author:                 Guodong
Author Email:           dgdenterprise@gmail.com
URL:                    https://github.com/DingGuodong/LinuxBashShellScriptForOps
Download URL:           https://github.com/DingGuodong/LinuxBashShellScriptForOps/tarball/master
Create Date:            2018/1/2
Create Time:            16:28
Description:            get the certificate's issuer and the valid days count
Long Description:       check website https certificate status
References:             https://gist.github.com/horacioibrahim/9413241
                        https://serverlesscode.com/post/ssl-expiration-alerts-with-lambda/
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
Programming Language:   Python :: 3
Topic:                  Utilities
 """
import datetime
import socket
import ssl
import sys

import certifi
import time

used_in_zabbix = False


def get_cert_info(hostname):
    global used_in_zabbix

    ssl_context = ssl.create_default_context(cafile=certifi.where())
    ssl_conn = None
    max_tries = 3
    tried_time = 0
    while True:
        try:
            ssl_conn = ssl_context.wrap_socket(
                socket.socket(socket.AF_INET),
                server_hostname=hostname,
            )
            ssl_conn.settimeout(30.0)
            ssl_conn.connect((hostname, 443))
            break
        except socket.error as e:
            tried_time += 1
            # such as 'socket.error: [Errno 10060]'
            if not used_in_zabbix:
                print(e, "try again, ({}/{})".format(max_tries, tried_time))
            if tried_time == max_tries:
                if not used_in_zabbix:
                    print("Exceed max number of try times, {}".format(max_tries))
                    sys.exit(1)
                else:
                    print(0)
                    sys.exit(0)
            time.sleep(1)
            if ssl_conn is not None:
                ssl_conn.close()
        except ValueError as e:
            # ValueError: attempt to connect already-connected SSLSocket!
            # Python 3.7 and higher raises ValueError if a socket is already connected
            if sys.version_info >= (3, 7):
                if not used_in_zabbix:
                    print(e)
                    exit(0)
                else:
                    print(0)
                    sys.exit(0)
            else:
                raise

    cert_info = ssl_conn.getpeercert()

    return cert_info


def get_cert_issuer(hostname):
    cert_info = get_cert_info(hostname)
    issuer = dict([tuple(x[0]) for x in cert_info.get('issuer')])
    common_name = issuer.get('commonName')
    return common_name


def get_cert_expiry_datetime(hostname):
    ssl_date_fmt = r'%b %d %H:%M:%S %Y %Z'
    cert_info = get_cert_info(hostname)  # 'notAfter': 'Jul 26 05:31:02 2021 GMT'
    # parse the string from the certificate into a Python datetime object
    return datetime.datetime.strptime(cert_info['notAfter'], ssl_date_fmt)


def get_cert_valid_days_remaining(hostname):
    """
    Get the number of days left in a cert's lifetime.
    import datetime; print((datetime.datetime.strptime("2021/7/26", "%Y/%m/%d") - datetime.datetime.now()).days)
    """
    expires = get_cert_expiry_datetime(hostname)
    return (expires - datetime.datetime.now()).days


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
    remain_days = get_cert_valid_days_remaining(hostname)
    issuer = get_cert_issuer(hostname)
    expires = get_cert_expiry_datetime(hostname)
    print("Domain: {}, ExpiredAfter: {}, DaysLeft: {}, Issuer: {}".format(
        hostname,
        expires,
        remain_days,
        issuer
    ))


if __name__ == '__main__':
    if len(sys.argv) == 1:
        show_domain_info("github.com")
        print(get_cert_valid_days_remaining("github.com"))
    elif len(sys.argv) == 2:
        used_in_zabbix = True
        # show_domain_info(sys.argv[-1])
        print(get_cert_valid_days_remaining(sys.argv[-1]))
    else:
        print("bad call. usage: {} <host>".format(sys.argv[0]))
        sys.exit(1)
