#!/usr/bin/python
# encoding: utf-8
# -*- coding: utf-8 -*-
"""
Created by PyCharm.
File Name:              LinuxBashShellScriptForOps:install_python27.py
Version:                0.0.1
Author:                 Guodong
Author Email:           dgdenterprise@gmail.com
URL:                    https://github.com/DingGuodong/LinuxBashShellScriptForOps
Download URL:           https://github.com/DingGuodong/LinuxBashShellScriptForOps/tarball/master
Create Date:            2018/11/7
Create Time:            14:39
Description:            
Long Description:       
References:             
Prerequisites:          pip install clint
Development Status:     3 - Alpha, 5 - Production/Stable
Environment:            Console
Intended Audience:      System Administrators, Developers, End Users/Desktop
License:                Freeware, Freely Distributable
Natural Language:       English, Chinese (Simplified)
Operating System:       POSIX :: Linux, Microsoft :: Windows
Programming Language:   Python :: 3

Topic:                  Utilities
 """
import sys
import os
from clint.textui.colored import red, green  # enable CLI Colors
import requests
import hashlib
import tarfile

PY27 = "2.7"
PY26 = "2.6"


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


def download(url, path=os.path.abspath(os.curdir)):
    filename = url.split('/')[-1]
    save = os.path.join(path, filename)

    print("Downloading '%s',\n save '%s' to '%s'" % (url, filename, save))
    response = requests.request("GET", url, stream=True, data=None, headers=None)

    with open(save, 'wb') as f:
        for chunk in response.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)
                f.flush()

    if os.path.isfile(save):
        print("Done: '%s'" % save)
        print("md5sum:", get_hash_sum(save, method="md5"))
        print("sha1sum:", get_hash_sum(save, method="sha1sum"))
        print("sha256sum:", get_hash_sum(save, method="sha256sum"))
    else:
        print("can not download", url)
        sys.exit(1)


def extract_tgz(src, dst=os.path.abspath(os.curdir)):
    with tarfile.open(src, "r:gz") as tar:
        tar.extractall(path=dst)


def install_python27():
    pass


# current python version
print(('Python %s on %s' % (sys.version, sys.platform)))

# `which python`
python_bin_path = [os.path.join(p, "python") for p in os.environ.get('PATH').split(os.pathsep)
                   if os.path.exists(os.path.join(p, "python"))]
if len(python_bin_path) > 0:
    print("default python interpreter path is %s" % python_bin_path[0])

if sys.version.startswith(PY27):
    print(green("the python interpreter is already %s version" % PY27))
    # exit(0)
elif not sys.version.startswith(PY26):
    print(red("the python interpreter is not %s version" % PY26))
    exit(2)

package_url = "https://www.python.org/ftp/python/2.7.15/Python-2.7.15.tgz"
package_md5sum = '045fb3440219a1f6923fefdabde63342'
package_file_size = 17496336

package_name = package_url.split('/')[-1]

if not os.path.exists(package_name):
    download(package_url)

extract_tgz(package_name)

