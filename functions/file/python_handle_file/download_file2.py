#!/usr/bin/python
# encoding: utf-8
# -*- coding: utf8 -*-
"""
Created by PyCharm.
File:               LinuxBashShellScriptForOps:download_file2.py
User:               Guodong
Create Date:        2016/9/14
Create Time:        9:40
 """
import requests
import requests.packages.urllib3
import os
import sys
import hashlib


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


requests.packages.urllib3.disable_warnings()

url = "https://raw.githubusercontent.com/racaljk/hosts/master/hosts"
filename = url.split('/')[-1]
save = os.path.join("/tmp", filename).replace("\\", "/")

print "Downloading '%s', save '%s' to '%s'" % (url, filename, save)
response = requests.request("GET", url, stream=True, data=None, headers=None)

total_length = int(response.headers.get("Content-Length"))
with open(save, 'wb') as f:
    for chunk in response.iter_content(chunk_size=1024):
        if chunk:
            f.write(chunk)
            f.flush()

if os.path.isfile(save):
    print "Done: '%s'" % save
    print "md5sum:", get_hash_sum(save, method="md5")
    print "sha1sum:", get_hash_sum(save, method="sha1sum")
    print "sha256sum:", get_hash_sum(save, method="sha256sum")
else:
    print "can not download", url
    sys.exit(1)
