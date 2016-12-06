#!/usr/bin/python
# encoding: utf-8
# -*- coding: utf8 -*-
"""
Created by PyCharm.
File:               LinuxBashShellScriptForOps:getHashSum.py
User:               Guodong
Create Date:        2016/12/6
Create Time:        16:56
 """
import hashlib
import os


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


def md5sum(filename):
    return get_hash_sum(filename)


def sha1sum(filename):
    return get_hash_sum(filename, method="sha1sum")


def sha256sum(filename):
    return get_hash_sum(filename, method="sha256sum")
