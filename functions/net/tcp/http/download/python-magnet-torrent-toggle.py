#!/usr/bin/python
# encoding: utf-8
# -*- coding: utf-8 -*-
"""
Created by PyCharm.
File Name:              LinuxBashShellScriptForOps:python-magnet-torrent-toggle.py
Version:                0.0.1
Author:                 Guodong
Author Email:           dgdenterprise@gmail.com
URL:                    https://github.com/DingGuodong/LinuxBashShellScriptForOps
Download URL:           https://github.com/DingGuodong/LinuxBashShellScriptForOps/tarball/master
Create Date:            2019/2/3
Create Time:            14:04
Description:            
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
import base64
import hashlib

import bencode

torrent = open('some.torrent', 'rb').read()
metadata = bencode.bdecode(torrent)
hashcontents = bencode.bencode(metadata['info'])
digest = hashlib.sha1(hashcontents).digest()
b32hash = base64.b32encode(digest)

print('magnet:?xt=urn:btih:%s' % b32hash)

# magnet:?xt=urn:btih:E412456AEEFC3DACA9CE1965B676347B8EA12F17
