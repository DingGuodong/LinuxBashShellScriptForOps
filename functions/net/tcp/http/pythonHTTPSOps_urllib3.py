#!/usr/bin/python
# encoding: utf-8
# -*- coding: utf8 -*-
"""
Created by PyCharm.
File:               LinuxBashShellScriptForOps:pythonHTTPSOps2.py
User:               Guodong
Create Date:        2016/11/22
Create Time:        14:05
 """
import certifi
import urllib3

# https://urllib3.readthedocs.io/en/latest/user-guide.html
http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED', ca_certs=certifi.where())
r = http.request('GET', 'https://registry-1.docker.io/v1/', timeout=4.0, retries=3)
print r.status
print r.data
