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
import hashlib
import os
import sys

import requests

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


def download_file(url, destfile):
    """
    method for downloading a file from an URL
    :param url: The URL of the file to be downloaded (assumed to be available via an HTTP GET request).
    :param destfile: The pathname where the downloaded file is to be saved.
    :return:
    """
    urllib3.disable_warnings()

    with open(destfile, 'wb') as fp:
        response = requests.request("GET", url, stream=False, headers=None)
        for chunk in response.iter_content(chunk_size=1024):
            if chunk:
                fp.write(chunk)
                fp.flush()


if __name__ == '__main__':
    wanted_url = "https://raw.githubusercontent.com/racaljk/hosts/master/hosts"
    filename = wanted_url.split('/')[-1]
    save = os.path.join("/tmp", filename).replace("\\", "/")

    print("Downloading '%s', save '%s' to '%s'" % (wanted_url, filename, save))

    download_file(wanted_url, save)

    if os.path.isfile(save):
        print("Saved: '%s'" % save)
        print("md5sum:", get_hash_sum(save, method="md5"))
        print("sha1sum:", get_hash_sum(save, method="sha1sum"))
        print("sha256sum:", get_hash_sum(save, method="sha256sum"))
    else:
        print("can not download", wanted_url)
        sys.exit(1)
