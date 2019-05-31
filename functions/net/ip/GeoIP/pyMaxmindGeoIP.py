#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created by PyCharm.
File Name:              LinuxBashShellScriptForOps:pyMaxmindGeoIP.py
Version:                0.0.1
Author:                 Guodong
Author Email:           dgdenterprise@gmail.com
URL:                    https://github.com/DingGuodong/LinuxBashShellScriptForOps
Download URL:           https://github.com/DingGuodong/LinuxBashShellScriptForOps/tarball/master
Create Date:            2019/4/28
Create Time:            18:23
Description:
Long Description:
References:             https://pythonhosted.org/python-geoip/
                        https://github.com/maxmind/GeoIP2-python

                        /usr/share/elasticsearch/modules/ingest-geoip/GeoLite2-ASN.mmdb
                        /usr/share/elasticsearch/modules/ingest-geoip/GeoLite2-City.mmdb
                        /usr/share/elasticsearch/modules/ingest-geoip/GeoLite2-Country.mmdb

Prerequisites:          python -m pip install --upgrade pip
                        pip install python-geoip-geolite2
                        pip install geoip2
Development Status:     3 - Alpha, 5 - Production/Stable
Environment:            Console
Intended Audience:      System Administrators, Developers, End Users/Desktop
License:                Freeware, Freely Distributable
Natural Language:       English, Chinese (Simplified)
Operating System:       POSIX :: Linux, Microsoft :: Windows
Programming Language:   Python :: 3
Topic:                  Utilities
 """

import datetime
import gzip
import os
import shutil
import tarfile

import geoip2.database
import requests
from geoip import geolite2


def untar(src, dst=os.path.abspath(os.curdir)):
    if os.path.isfile(dst):
        dst = os.path.dirname(dst)
    with tarfile.open(src, "r:gz") as tar:
        tar.extractall(path=dst)


def ungzip(src, dst):
    if os.path.exists(src) and os.path.exists(os.path.dirname(dst)):
        try:
            with gzip.open(src, 'rb') as f_in:
                with open(dst, 'wb') as f_out:
                    shutil.copyfileobj(f_in, f_out)
        except IOError as e:
            print(e)
            raise IOError("and maybe file is opened in another process")

    else:
        print("No such file or directory")


info = geolite2.get_info()
mmdb_filename = info.filename

# update mmdb
if info.date < datetime.datetime and info.date.strftime("%Y/%m/%d") == '2015/03/03':
    print(info)
    if not os.path.exists(info.filename + ".gz"):
        url = 'https://geolite.maxmind.com/download/geoip/database/GeoLite2-City.mmdb.gz'
        with open(mmdb_filename + ".gz", 'wb') as fp:
            response = requests.request("GET", url, stream=False)
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    fp.write(chunk)
                    fp.flush()
    else:
        del info
        del geolite2
        ungzip(mmdb_filename + ".gz", mmdb_filename)
        from geoip import geolite2

        info = geolite2.get_info()
        print(info)
else:
    print(info)

# read data from db
reader = geoip2.database.Reader(mmdb_filename)
response = reader.city("114.114.114.114")

# response
print(response.country.iso_code)
print(response.country.names.get("zh-CN"))
print(response.city.names.get("zh-CN"))
