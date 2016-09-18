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

import urllib
import requests.packages.urllib3

requests.packages.urllib3.disable_warnings()

url = "https://raw.githubusercontent.com/racaljk/hosts/master/hosts"
urllib.urlretrieve(url, filename="hosts")
