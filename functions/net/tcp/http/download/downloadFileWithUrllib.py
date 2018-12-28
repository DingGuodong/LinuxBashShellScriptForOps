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

import hashlib
import os
import socket
import sys
import urllib

from timeout import timeout

try:
    from requests.packages import urllib3
except ImportError:
    import urllib3


def get_hash_sum(name, method="md5", block_size=65536):
    if not os.path.exists(name):
        raise RuntimeError("cannot open '%s' (No such file or directory)" % name)
    if not os.path.isfile(name):
        raise RuntimeError("'%s' :not a regular file" % name)

    if "md5" in method:
        checksum = hashlib.md5()
    elif "sha1" in method:
        checksum = hashlib.sha1()
    elif "sha256" in method:
        checksum = hashlib.sha256()
    else:
        raise RuntimeError("unsupported method %s" % method)

    # if os.path.exists(filename) and os.path.isfile(filename):
    with open(name, 'rb') as f:
        buf = f.read(block_size)
        while len(buf) > 0:
            checksum.update(buf)
            buf = f.read(block_size)
        if checksum is not None:
            return checksum.hexdigest()
        else:
            return checksum


if __name__ == '__main__':
    urllib3.disable_warnings()

    mswindows = (sys.platform == "win32")  # learning from 'subprocess' module

    url = "https://raw.githubusercontent.com/racaljk/hosts/master/hosts"
    filename = url.split('/')[-1]
    save = os.path.join("/tmp", filename).replace("\\", "/")

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
        print "Saved: '%s'" % save
        print "md5sum:", get_hash_sum(save, method="md5")
        print "sha1sum:", get_hash_sum(save, method="sha1sum")
        print "sha256sum:", get_hash_sum(save, method="sha256sum")
    else:
        print "can not download", url
        sys.exit(1)
