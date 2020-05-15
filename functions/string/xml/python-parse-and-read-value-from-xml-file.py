#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created by PyCharm.
File Name:              LinuxBashShellScriptForOps:python-parse-xml.py
Version:                0.0.1
Author:                 dgden
Author Email:           dgdenterprise@gmail.com
URL:                    https://github.com/DingGuodong/LinuxBashShellScriptForOps
Download URL:           https://github.com/DingGuodong/LinuxBashShellScriptForOps/tarball/master
Create Date:            2020/5/14
Create Time:            14:41
Description:            use xpath to get value in xml element without `for` loop
Long Description:       
References:             
Prerequisites:          []
Development Status:     3 - Alpha, 5 - Production/Stable
Environment:            Console
Intended Audience:      System Administrators, Developers, End Users/Desktop
License:                Freeware, Freely Distributable
Natural Language:       English, Chinese (Simplified)
Operating System:       POSIX :: Linux, Microsoft :: Windows
Programming Language:   Python :: 2.6
Programming Language:   Python :: 2.7
Topic:                  Utilities
 """
from io import BytesIO, StringIO

from lxml import etree, objectify

xml_string = '''<?xml version="1.0" encoding="utf-8" ?>
<connectionList>
    <connection id="3205" name="xxxx1"
                connectionString="Data Source=10.25.20.52,1433;Initial Catalog=dbname;Catalog=username;PassWord=password;Persist Security Info=True;Min Pool Size=1;Connect Timeout=9000000"/>
    <connection id="3206" name="xxxx2"
                connectionString="Data Source=10.25.20.52,1433;Initial Catalog=dbname;Catalog=username;PassWord=password;Persist Security Info=True;Min Pool Size=1;Connect Timeout=9000000"/>
</connectionList>
'''

parser = etree.XMLParser()
root = etree.parse(BytesIO(xml_string.encode("utf-8")), parser).getroot()

if root is None:  # use method 2
    root = objectify.parse(StringIO(xml_string), parser=parser).getroot()
else:
    for element in root:
        print(element.tag, element.attrib.get("name"), element.attrib.get("id"))

    for item in root.findall("connection"):
        print(item.tag, item.attrib.get("name"), item.attrib.get("id"))

    # use xpath to get value in xml element without `for` loop
    result_list = root.xpath("/connectionList/connection[@id=3205]")
    if len(result_list) > 0:
        print(result_list[0].attrib.get("connectionString"))
    else:
        print("")
