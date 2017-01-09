#!/usr/bin/python
# encoding: utf-8
# -*- coding: utf8 -*-
"""
Created by PyCharm.
File:               LinuxBashShellScriptForOps:downloadFileWithPyCurl.py
User:               Guodong
Create Date:        2017/1/3
Create Time:        11:58
 """
import pycurl
import os
import certifi

url = "https://raw.githubusercontent.com/racaljk/hosts/master/hosts"
filename = url.split('/')[-1]
save = os.path.join("/tmp", filename).replace("\\", "/")

# http://pycurl.io/docs/latest/index.html
# http://pycurl.io/docs/latest/quickstart.html#retrieving-a-network-resource
# As long as the file is opened in binary mode, both Python 2 and Python 3
# can write response body to it without decoding.
with open(save, 'wb') as f:
    c = pycurl.Curl()
    c.setopt(c.URL, url)
    c.setopt(c.CAINFO, certifi.where())  # c.setopt(pycurl.SSL_VERIFYPEER, False)  # useful for HTTPS connection
    c.setopt(c.FOLLOWLOCATION, True)
    c.setopt(c.CONNECTTIMEOUT, 10)
    c.setopt(c.TIMEOUT, 10)
    c.setopt(c.WRITEDATA, f)
    c.perform()
    c.close()
