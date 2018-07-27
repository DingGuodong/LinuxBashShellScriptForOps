#!/usr/bin/python
# encoding: utf-8
# -*- coding: utf-8 -*-
"""
Created by PyCharm.
File Name:              LinuxBashShellScriptForOps:pyXMLParser2.py
Version:                0.0.1
Author:                 Guodong
Author Email:           dgdenterprise@gmail.com
URL:                    https://github.com/DingGuodong/LinuxBashShellScriptForOps
Download URL:           https://github.com/DingGuodong/LinuxBashShellScriptForOps/tarball/master
Create Date:            2018/7/27
Create Time:            9:25
Description:            an example about find tag or text in XML file
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
import requests

try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET
from lxml import etree
import os
import re

test_xml_file_url = 'https://raw.githubusercontent.com/apache/tomcat/trunk/conf/server.xml'
xml_filename = 'xml_file.txt'


def get_xml_file():
    with open(xml_filename, 'wb') as f:
        f.write(requests.get(test_xml_file_url).content)


if not os.path.exists(xml_filename):
    get_xml_file()

with open(xml_filename, 'r') as f:
    xml_string = f.read()

tree = etree.fromstring(xml_string)
etree.strip_tags(tree, etree.Comment)
xml_string_without_comment = etree.tostring(tree)

xml_string_without_comment_blank = re.sub('\s*\n', '\n', xml_string_without_comment)  # remove blank lines
# wu1 = os.linesep.join([line for line in xml_string_without_comment.splitlines() if line.strip()])  # line separators
# wu2 = "".join([line for line in xml_string_without_comment.splitlines(True) if line.strip()])
# wu3 = "".join(filter(str.strip, xml_string_without_comment.splitlines(True)))

with open(xml_filename, 'w') as f:
    f.write(xml_string_without_comment_blank)

new_tree = ET.ElementTree(file=xml_filename)

for element in new_tree.findall('Service/Connector'):
    print(element.attrib)
