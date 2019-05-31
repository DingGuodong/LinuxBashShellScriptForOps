#!/usr/bin/python
# encoding: utf-8
# -*- coding: utf8 -*-
"""
Created by PyCharm.
File:               LinuxBashShellScriptForOps:download_file.py
User:               Guodong
Create Date:        2016/9/13
Create Time:        15:41

pip install urllib3 certifi
or
pip install urllib3[secure]

 """

import hashlib
import os
import sys

import socket

try:
    from requests.packages import urllib3
except ImportError:
    import urllib3


def download_file(url, path=""):
    chunk_size = 2 ** 16
    if path == "":
        http = urllib3.PoolManager()
        r = http.request('GET', url, preload_content=False)

        with open(path, 'wb') as out:
            while True:
                data = r.read(chunk_size)
                if not data:
                    break
                out.write(data)

        r.release_conn()


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
        print("Downloading", url)
        download_file(url, save)
    else:
        assert sys.platform == "linux2", "please run this script on Linux"
        from timeout import timeout  # upstream bug: Python3 not compatible
        with timeout(timeout=10.0):
            download_file(url, save)

    if os.path.isfile(save):
        print("Saved: '%s'" % save)
        print("md5sum:", get_hash_sum(save, method="md5"))
        print("sha1sum:", get_hash_sum(save, method="sha1sum"))
        print("sha256sum:", get_hash_sum(save, method="sha256sum"))
    else:
        print("can not download", url)
        sys.exit(1)
