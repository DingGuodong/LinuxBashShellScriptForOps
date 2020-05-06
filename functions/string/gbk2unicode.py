#!/usr/bin/python
# encoding: utf-8
# -*- coding: utf8 -*-
"""
Created by PyCharm.
File:               LinuxBashShellScriptForOps:unicode2gbk.py
User:               Guodong
Create Date:        2016/12/12
Create Time:        9:52
 """
import sys

print('\xbe\xdc\xbe\xf8\xb7\xc3\xce\xca\xa1\xa3'.decode("gbk"))
print(unicode('\xbe\xdc\xbe\xf8\xb7\xc3\xce\xca\xa1\xa3', 'gbk'))

print(sys.getdefaultencoding())  # Out: 'ascii'
print(sys.stdout.encoding)  # Out: 'UTF-8'
if 'utf8' not in sys.getdefaultencoding():
    # https://stackoverflow.com/questions/3828723/why-should-we-not-use-sys-setdefaultencodingutf-8-in-a-py-script
    reload(sys)  # The reload() call restores the deleted attribute.
    sys.setdefaultencoding("UTF-8")
    print(sys.getdefaultencoding())  # Out: 'UTF-8'
