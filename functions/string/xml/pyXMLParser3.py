#!/usr/bin/python
# encoding: utf-8
# -*- coding: utf-8 -*-
"""
Created by PyCharm.
File Name:              LinuxBashShellScriptForOps:pyXMLParser3.py
Version:                0.0.1
Author:                 Guodong
Author Email:           dgdenterprise@gmail.com
URL:                    https://github.com/DingGuodong/LinuxBashShellScriptForOps
Download URL:           https://github.com/DingGuodong/LinuxBashShellScriptForOps/tarball/master
Create Date:            2018/7/27
Create Time:            15:39
Description:            find text with a XML file with namespace
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
try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET

xml_filename = 'config.xml'  # a xml file with namespace from a stranger in a same QQ group

if ET.parse(xml_filename):
    pass
else:
    print('invalid xml file')

# for _, elem in ET.iterparse(xml_filename):
#     if elem.tag == '{http://xmlns.oracle.com/weblogic/domain}server':
#         print(elem)

tree = ET.ElementTree(file=xml_filename)
for elem in tree.findall('{http://xmlns.oracle.com/weblogic/domain}server'):
    listen_port = elem.find('{http://xmlns.oracle.com/weblogic/domain}listen-port')  # namespaces = ‘{http://xxxx}'
    machine = elem.find('{http://xmlns.oracle.com/weblogic/domain}machine')
    name = elem.find('{http://xmlns.oracle.com/weblogic/domain}name')
    if listen_port is not None:
        print((" ".join((listen_port.text, machine.text, name.text))))
