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
Description:            an example of find tag or text in XML file with built modules
Long Description:
References:             
Prerequisites:          []
Development Status:     3 - Alpha, 5 - Production/Stable
Environment:            Console
Intended Audience:      System Administrators, Developers, End Users/Desktop
License:                Freeware, Freely Distributable
Natural Language:       English, Chinese (Simplified)
Operating System:       POSIX :: Linux, Microsoft :: Windows
Programming Language:   Python :: 3

Topic:                  Utilities
 """
import requests

try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET
try:
    import io as StringIO
except ImportError:
    import io

test_xml_file_url = 'https://raw.githubusercontent.com/apache/tomcat/trunk/conf/server.xml'
xml_string = requests.get(test_xml_file_url).content
xml_file = io.StringIO(xml_string)

new_tree = ET.ElementTree(file=xml_file)

for element in new_tree.findall('Service/Connector'):  # <type 'Element'>
    # print(element.attrib)
    if element.get('protocol') == 'HTTP/1.1':
        print(element.get('port'))
