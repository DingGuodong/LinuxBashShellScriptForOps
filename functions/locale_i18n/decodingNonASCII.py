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
Description:            try decoding some string(type: str) with right encoding
Long Description:       Deep understanding of Python2 encoding:
                            py2.str("xxx")  = py2.str("xxx") + py2.bytes(b"") + py2.bytes("\xxx")
                            py2.unicode(u"") = py2.unicode(u"")

                            py3.str("xxx")  = py2.str("xxx") + py2.unicode(u"")
                            py3.bytes(b"") = py2.bytes(b"") + py2.bytes("\xxx")
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
import sys


def decoding(text):
    import locale
    encoding = locale.getpreferredencoding()

    if isinstance(text, unicode):
        return text
    elif isinstance(text, str):
        try:
            return text.decode(encoding)
        except UnicodeDecodeError:
            return text.decode("utf-8")
    else:
        return text


def decoding_deprecated(text):
    import sys
    import codecs
    import locale

    if isinstance(text, unicode):
        return text
    elif isinstance(text, (basestring, str)):
        pass
    else:
        return text  # do not need decode, return original object if type is not instance of string type
        # raise RuntimeError("expected type is str, but got {type} type".format(type=type(text)))

    mswindows = (sys.platform == "win32")

    try:
        encoding = locale.getdefaultlocale()[1] or ('ascii' if not mswindows else 'gbk')
        codecs.lookup(encoding)  # codecs.lookup('cp936').name == 'gbk'
    except Exception as _:
        del _
        encoding = 'ascii' if not mswindows else 'gbk'  # 'gbk' is Windows default encoding in Chinese language 'zh-CN'

    msg = text
    if mswindows:
        try:
            msg = text.decode(encoding)
            return msg
        except (UnicodeDecodeError, UnicodeEncodeError):
            pass
    return msg


if __name__ == '__main__':
    # The boolean values of all these expressions are True
    isinstance('\xd6\xd0\xb9\xfa\xba\xba\xd7\xd6'.decode('gbk'), unicode)
    isinstance('\xe4\xb8\xad\xe5\x9b\xbd\xe6\xb1\x89\xe5\xad\x97'.decode('utf8'), unicode)
    isinstance('中国汉字'.decode('utf8'), unicode)  # only works in some case, such as declare 'utf8' at top
    isinstance(u'中国汉字', unicode)
    isinstance(u'中国汉字'.encode('gbk'), str)
    isinstance(u'中国汉字'.encode('gbk'), basestring)

    # This function(sys._getframe()) should be used for internal and specialized purposes only.
    print sys._getframe().f_lineno, decoding(u"中国汉字")  # print line no. to make read result easy

    print sys._getframe().f_lineno, decoding("中国汉字".decode('utf8').encode('gbk'))
    print sys._getframe().f_lineno, decoding("中国汉字")
    print sys._getframe().f_lineno, decoding(u"中国汉字")
    print sys._getframe().f_lineno, decoding('\xd6\xd0\xb9\xfa\xba\xba\xd7\xd6')
    print sys._getframe().f_lineno, decoding('\xe4\xb8\xad\xe5\x9b\xbd\xe6\xb1\x89\xe5\xad\x97')

    print sys._getframe().f_lineno, len('\xd6\xd0\xb9\xfa\xba\xba\xd7\xd6') % 2 == 0  # gbk
    print len('\xe4\xb8\xad\xe5\x9b\xbd\xe6\xb1\x89\xe5\xad\x97') % 3 == 0  # utf-8

    with open("gbk.txt", 'w+') as fp:  # encoding with default locale
        fp.write(u'中国汉字'.encode('gbk'))
        fp.write('中国汉字'.decode("utf-8").encode("gbk"))

    with open("utf8.txt", 'w+') as fp:  # encoding with utf-8
        fp.write(u'中国汉字'.encode("utf-8"))
        fp.write('中国汉字')

    with open("bytes.txt", 'w+') as fp:  # encoding with utf-8
        fp.write(b'\xe4\xb8\xad\xe5\x9b\xbd\xe6\xb1\x89\xe5\xad\x97')
        fp.write('\xe4\xb8\xad\xe5\x9b\xbd\xe6\xb1\x89\xe5\xad\x97')
