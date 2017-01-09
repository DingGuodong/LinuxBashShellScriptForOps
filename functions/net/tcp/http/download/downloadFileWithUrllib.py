#!/usr/bin/python
# encoding: utf-8
# -*- coding: utf8 -*-
"""
Created by PyCharm.
File:               LinuxBashShellScriptForOps:download_file.py
User:               Guodong
Create Date:        2016/9/13
Create Time:        15:41
 """

import os
import sys
import urllib
import requests.packages.urllib3
import socket
import hashlib
from timeout import timeout


def get_hash_sum(filename, method="md5", block_size=65536):
    if not os.path.exists(filename):
        raise RuntimeError("cannot open '%s' (No such file or directory)" % filename)
    if not os.path.isfile(filename):
        raise RuntimeError("'%s' :not a regular file" % filename)

    if "md5" in method:
        checksum = hashlib.md5()
    elif "sha1" in method:
        checksum = hashlib.sha1()
    elif "sha256" in method:
        checksum = hashlib.sha256()
    else:
        raise RuntimeError("unsupported method %s" % method)

    # if os.path.exists(filename) and os.path.isfile(filename):
    with open(filename, 'rb') as f:
        buf = f.read(block_size)
        while len(buf) > 0:
            checksum.update(buf)
            buf = f.read(block_size)
        if checksum is not None:
            return checksum.hexdigest()
        else:
            return checksum


mswindows = (sys.platform == "win32")  # learning from 'subprocess' module

url = "https://raw.githubusercontent.com/racaljk/hosts/master/hosts"
filename = url.split('/')[-1]
save = os.path.join("/tmp", filename).replace("\\", "/")

requests.packages.urllib3.disable_warnings()

if mswindows:
    # global socket timeout
    socket.setdefaulttimeout(10.0)
    print "Downloading", url
    urllib.urlretrieve(url, filename=save)
else:
    assert sys.platform == "linux2", "please run this script on Windows or Linux"
    with timeout(timeout=10.0):
        urllib.urlretrieve(url, filename=save)

if os.path.isfile(save):
    print "Done:", save
    print "md5sum:", get_hash_sum(save, method="md5")
    print "sha1sum:", get_hash_sum(save, method="sha1sum")
    print "sha256sum:", get_hash_sum(save, method="sha256sum")
else:
    print "can not download", url
    sys.exit(1)
