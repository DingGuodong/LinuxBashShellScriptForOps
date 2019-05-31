#!/usr/bin/python
# encoding: utf-8
# -*- coding: utf-8 -*-
"""
Created by PyCharm.
File Name:              LinuxBashShellScriptForOps:pyCheckHTTPServiceStatus.py
Version:                0.0.1
Author:                 Guodong
Author Email:           dgdenterprise@gmail.com
URL:                    https://github.com/DingGuodong/LinuxBashShellScriptForOps
Download URL:           https://github.com/DingGuodong/LinuxBashShellScriptForOps/tarball/master
Create Date:            2018/8/8
Create Time:            11:11
Description:            
Long Description:       
References:             
Prerequisites:          pip install python-ping
Development Status:     3 - Alpha, 5 - Production/Stable
Environment:            Console
Intended Audience:      System Administrators, Developers, End Users/Desktop
License:                Freeware, Freely Distributable
Natural Language:       English, Chinese (Simplified)
Operating System:       POSIX :: Linux, Microsoft :: Windows
Programming Language:   Python :: 3

Topic:                  Utilities
 """
import requests

http_service_config = {
    "name": '',
    "url": 'https://webpush.wx.qq.com:80/cgi-bin/mmwebwx-bin/synccheck',
    "post": '',
    "variables": '',
    "headers": '',
    "timeout": '',
    "header_only": False,
    "required_string": '',
    "required_status_code": 200,
    "http_proxy": '',
    "https_proxy": '',
    "authentication": "",
}


def check_http():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/68.0.3440.84 Safari/537.36"
    }
    url = http_service_config.get('url')
    required_string = http_service_config.get('required_string')
    required_status_code = http_service_config.get('required_status_code')

    try:
        request = requests.get(url, headers=headers)
    except Exception:
        return

    status_code = request.status_code
    content = request.content

    if required_status_code == status_code and required_string in content:
        status = 'OK'
        match = True
    else:
        status = 'ERROR'
        match = False

    print("Status: {status}\nStatus code: {code}\nKeyword match: {match}".format(status=status, code=status_code,
                                                                                 match=match))


def get_domain_name():
    from urllib.parse import urlparse
    url = http_service_config.get('url')
    parsed_uri = urlparse(url)
    # host = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)
    host = "{uri.netloc}".format(uri=parsed_uri)
    if ":" in host:
        host, port = host.split(":")
    else:
        if url.startswith("https"):
            port = 443
        else:
            port = 80
    return host, port


def check_name_resolve():
    import dns.resolver

    host = get_domain_name()[0]

    query = dns.resolver.Resolver()
    query.nameservers = ['114.114.114.114']
    query.timeout = 1.0
    query.lifetime = 3.0
    answer = query.query(host, 'A').response.answer
    for record in answer[-1]:
        print("A records: %s" % record)


def check_network():
    import ping
    host = get_domain_name()[0]
    ping.verbose_ping(host)


def check_port():
    import socket
    host, port = get_domain_name()
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect((host, int(port)))
        s.shutdown(socket.AF_INET)
        print("Port %s is open." % port)
    except socket.error:
        print("Port %s is unreachable." % port)
    finally:
        s.close()


if __name__ == '__main__':
    check_http()
    check_name_resolve()
    check_network()
    check_port()
