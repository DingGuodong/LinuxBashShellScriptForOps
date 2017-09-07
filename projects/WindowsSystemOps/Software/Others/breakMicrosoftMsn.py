#!/usr/bin/python
# encoding: utf-8
# -*- coding: utf8 -*-
"""
Created by PyCharm.
File:               LinuxBashShellScriptForOps:breakMicrosoftMsn.py
User:               Guodong
Create Date:        2017/9/7
Create Time:        14:01
Description:        Block MSN web site forever by using firewall after using dns block failed
References:         
 """
import sys
import subprocess
import codecs
import locale

mswindows = (sys.platform == "win32")  # learning from 'subprocess' module
linux = (sys.platform == "linux2")


def get_system_encoding():
    """
    The encoding of the default system locale but falls back to the given
    fallback encoding if the encoding is unsupported by python or could
    not be determined.  See tickets #10335 and #5846
    """
    try:
        encoding = locale.getdefaultlocale()[1] or 'ascii'
        codecs.lookup(encoding)
    except Exception:
        encoding = 'ascii'
    return encoding


DEFAULT_LOCALE_ENCODING = get_system_encoding()


def get_status_code():
    import requests

    url = "https://www.msn.com/spartan/ientp"
    querystring = {"locale": "zh-CN", "market": "CN", "enableregulatorypsm": "0", "NTLogo": "0", "IsFRE": "0"}
    headers = {
        'cache-control': "no-cache",
    }
    try:
        response = requests.request("GET", url, headers=headers, params=querystring)
        return response.status_code
    except requests.ConnectionError:
        return 502


def get_ip_from_domain(domain):
    import dns.resolver
    query = dns.resolver.Resolver()
    query.nameservers = ['180.76.76.76']
    query.timeout = 1.0
    query.lifetime = 3.0
    query.cache = False
    answer = query.query(domain)
    records = list()
    for item in list(answer):
        records.append(str(item))
    return records


def get_domain_from_url(url):
    import urllib
    proto, rest = urllib.splittype(url)
    domain, rest = urllib.splithost(rest)
    return domain


def block_ip(ip):
    command = r"netsh advfirewall firewall add rule name=\"block_ip_{n_ip}\"" \
              r" dir=out protocol=tcp remoteip={r_ip} action=block profile=any ".format(n_ip=ip, r_ip=ip)
    if mswindows:
        print "Run local command \'{command}\' on Windows...".format(command=command)

        proc_obj = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE,
                                    stderr=subprocess.STDOUT)
        result = proc_obj.stdout.read().lower().decode(DEFAULT_LOCALE_ENCODING)
        if result:
            print result

    else:
        print "Windows Supported Only. Aborted!"
        sys.exit(1)


if __name__ == '__main__':
    url_to_block = "https://www.msn.com"
    while get_status_code() == 200:
        ip_list = get_ip_from_domain(get_domain_from_url(url_to_block))
        for host in ip_list:
            block_ip(host)
