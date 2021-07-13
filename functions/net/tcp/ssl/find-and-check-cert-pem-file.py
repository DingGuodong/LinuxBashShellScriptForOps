#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Created by PyCharm.
File Name:              LinuxBashShellScriptForOps:get-ssl-cert-info-from-pem-file.py
Version:                0.0.1
Author:                 dgden
Author Email:           dgdenterprise@gmail.com
URL:                    https://github.com/DingGuodong/LinuxBashShellScriptForOps
Download URL:           https://github.com/DingGuodong/LinuxBashShellScriptForOps/tarball/master
Create Date:            2021/7/7
Create Time:            11:11
Description:            find and check certificates from pem file.
Long Description:
References:
Prerequisites:          pip install --upgrade pip
                        pip install pyOpenSSL python-dateutil

                        pip3 install --upgrade pip
                        pip3 install setuptools_rust pyOpenSSL python-dateutil
for python3.5
    wget https://bootstrap.pypa.io/pip/3.5/get-pip.py
    sudo python3.5 get-pip.py
for pyhton3.6+
    curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
    python3.6 get-pip.py

Development Status:     3 - Alpha, 5 - Production/Stable
Environment:            Console
Intended Audience:      System Administrators, Developers, End Users/Desktop
License:                Freeware, Freely Distributable
Natural Language:       English, Chinese(Simplified)
Operating System:       POSIX :: Linux, Microsoft :: Windows
Programming Language:   Python :: 2.6
Programming Language:   Python :: 2.7
Programming Language:   Python :: 3
Topic:                  Utilities
 """
import os

import OpenSSL
from OpenSSL.crypto import load_certificate
from dateutil import parser
import datetime
from dateutil.tz import tzutc

cert_dirs = [
    "/home/data/sync/certs/live",
    "/etc/letsencrypt/live",
    "/etc/certs/live"
]


def get_certificate_info(path):
    with open(path) as fp:
        cert_content = fp.read()
    cert = load_certificate(OpenSSL.crypto.FILETYPE_PEM, cert_content.encode())
    is_expired = cert.has_expired()
    issue_to = str(dict(cert.get_subject().get_components()).get(b'CN').decode())

    remain_days = (parser.parse(cert.get_notAfter()) - datetime.datetime.now(tz=tzutc())).days
    return is_expired, remain_days, issue_to


def find_certificates(path):
    for top, dirs, nondirs in os.walk(path):
        for filename in nondirs:
            full_path_to_filename = os.path.join(top, filename)
            if full_path_to_filename.endswith("fullchain.pem"):
                yield full_path_to_filename


if __name__ == '__main__':
    for cert_dir in cert_dirs:
        for cert_file in find_certificates(cert_dir):
            print(cert_file, get_certificate_info(cert_file))
