#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created by PyCharm.
File Name:              LinuxBashShellScriptForOps:get-ssl-cert-info-from-pem-file.py
Version:                0.0.1
Author:                 dgden
Author Email:           dgdenterprise@gmail.com
URL:                    https://github.com/DingGuodong/LinuxBashShellScriptForOps
Download URL:           https://github.com/DingGuodong/LinuxBashShellScriptForOps/tarball/master
Create Date:            2021/3/24
Create Time:            11:11
Description:            get SSL certificate from PEM file
Long Description:       
References:             
Prerequisites:          []
Development Status:     3 - Alpha, 5 - Production/Stable
Environment:            Console
Intended Audience:      System Administrators, Developers, End Users/Desktop
License:                Freeware, Freely Distributable
Natural Language:       English, Chinese(Simplified)
Operating System:       POSIX :: Linux, Microsoft :: Windows
Programming Language:   Python :: 2.6
Programming Language:   Python :: 2.7
Topic:                  Utilities
 """

# from ssl import DER_cert_to_PEM_cert
import OpenSSL
from OpenSSL.crypto import load_certificate
from dateutil import parser

with open("5366531_www.example.com.pem") as fp:
    content = fp.read()

cert = load_certificate(OpenSSL.crypto.FILETYPE_PEM, content)


def to_unicode_or_bust(obj, encoding='utf-8'):
    """
    convert non-unicode object to unicode object
    :param obj: str object or unicode
    :param encoding:
    :return:
    """
    if isinstance(obj, basestring):
        if not isinstance(obj, unicode):
            obj = unicode(obj, encoding)
    else:
        return str(obj)

    return obj


def print_v2(*args):
    print("".join([to_unicode_or_bust(x) for x in args]))


print_v2("颁发者: ", cert.get_issuer().commonName)
print_v2("颁发给: ", dict(cert.get_subject().get_components()).get('CN'))
print_v2("有效期从: ", parser.parse(cert.get_notBefore()).strftime('%Y-%m-%d %H:%M:%S'))
print_v2("到: ", parser.parse(cert.get_notAfter()).strftime('%Y-%m-%d %H:%M:%S'))
print_v2("证书是否已经过期: ", cert.has_expired())

cert_name_map = {
    "CN": "通用名称 ",
    "OU": "机构单元名称",
    "O": "机构名 ",
    "L": "地理位置",
    "S": "州/省名",
    "C": "国名"
}

for item in cert.get_issuer().get_components():
    print_v2(cert_name_map.get(item[0]), ": ", item[1])
