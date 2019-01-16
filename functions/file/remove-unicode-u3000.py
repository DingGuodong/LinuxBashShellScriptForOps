#!/usr/bin/python
# encoding: utf-8
# -*- coding: utf-8 -*-
"""
Created by PyCharm.
File Name:              LinuxBashShellScriptForOps:remove-unicode-u3000.py
Version:                0.0.1
Author:                 Guodong
Author Email:           dgdenterprise@gmail.com
URL:                    https://github.com/DingGuodong/LinuxBashShellScriptForOps
Download URL:           https://github.com/DingGuodong/LinuxBashShellScriptForOps/tarball/master
Create Date:            2019/1/16
Create Time:            15:28
Description:            remove u'\u3000'（IDEOGRAPHIC SPACE, '\xe3\x80\x80'(utf-8)) in Python
Long Description:       
References:             $ cat -A gitdiff.log
                        $ file <filename> # determine file type, Determines file type using "magic" numbers
                        https://www.cnblogs.com/BlackStorm/p/6359005.html
                        http://120.52.51.16/www.unicode.org/charts/PDF/U3000.pdf
                        https://stackoverflow.com/questions/36422107/how-to-convert-crlf-to-lf-on-a-windows-machine-in-python
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
# Method1: using Linux sed command: `sed -i 's/\xe3\x80\x80/ /g' gitdiff.log`

# Method2:
"""
CRLF to LF line separator
Important: using Binary Mode 'rb' or 'wb'
We need to make sure that we open the file both times in binary mode (mode='rb' and mode='wb') 
for the conversion to work.
When opening files in text mode (mode='r' or mode='w' without b), 
the platform's native line endings (\r\n on Windows and \r on old Mac OS versions) are automatically 
converted to Python's Unix-style line endings: \n. 
So the call to content.replace() couldn't find any line endings to replace.
In binary mode, no such conversion is done.
"""
with open("gitdiff_m.log", 'wb') as fp1:
    with open("gitdiff.log", 'rb') as fp2:  # file gitdiff.log: gitdiff.log: UTF-8 Unicode text
        for line in fp2:
            fp1.write(line.decode("utf-8").replace(u'\u3000', ' ').encode("utf-8"))
