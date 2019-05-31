#!/usr/bin/python
# encoding: utf-8
# -*- coding: utf8 -*-
"""
Created by PyCharm.
File Name:              LinuxBashShellScriptForOps:decodingNonASCII.py
Version:                0.0.1
Author:                 Guodong
Author Email:           dgdenterprise@gmail.com
URL:                    https://github.com/DingGuodong/LinuxBashShellScriptForOps
Download URL:           https://github.com/DingGuodong/LinuxBashShellScriptForOps/tarball/master
Create Date:            2017/11/28
Create Time:            15:13
Description:            try decoding str and bytes with utf-8 encoding
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
import sys


def always_to_utf8(text):
    import locale

    encoding = locale.getpreferredencoding()
    if isinstance(text, bytes):
        try:
            return text.decode(encoding)
        except UnicodeDecodeError:
            return text.decode("utf-8")

    else:
        return text  # do not need decode, return original object if type is not instance of string type
        # raise RuntimeError("expected type is str, but got {type} type".format(type=type(text)))


if __name__ == '__main__':
    # The boolean values of all these expressions are True
    isinstance(b'\xd6\xd0\xb9\xfa\xba\xba\xd7\xd6'.decode('gbk'), str)
    isinstance(b'\xe4\xb8\xad\xe5\x9b\xbd\xe6\xb1\x89\xe5\xad\x97'.decode('utf8'), str)
    isinstance('中国汉字', str)  # only works in some case, such as declare 'utf8' at top
    isinstance(u'中国汉字', str)
    isinstance(u'中国汉字'.encode('gbk'), bytes)

    # This function(sys._getframe()) should be used for internal and specialized purposes only.
    print(sys._getframe().f_lineno, u"中国汉字")  # print line no. to make read result easy
    print(sys._getframe().f_lineno, "中国汉字")  # print line no. to make read result easy

    print(always_to_utf8(b'\xe4\xb8\xad\xe5\x9b\xbd\xe6\xb1\x89\xe5\xad\x97'))
    print(always_to_utf8(b'\xd6\xd0\xb9\xfa\xba\xba\xd7\xd6'))
    print(always_to_utf8(u'中国汉字'))
    print(always_to_utf8('中国汉字'))

    with open("always-using-utf8.default.txt", 'w+') as fp:  # encoding with default locale
        fp.write(u'中国汉字')
        fp.write('中国汉字')

    with open("always-using-utf8.utf8.txt", 'w+', encoding="utf-8") as fp:  # encoding with utf-8
        fp.write(u'中国汉字')
        fp.write('中国汉字')

