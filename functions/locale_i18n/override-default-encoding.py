#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created by PyCharm.
File Name:              LinuxBashShellScriptForOps:override-default-encoding.py
Version:                0.0.1
Author:                 dgden
Author Email:           dgdenterprise@gmail.com
URL:                    https://github.com/DingGuodong/LinuxBashShellScriptForOps
Download URL:           https://github.com/DingGuodong/LinuxBashShellScriptForOps/tarball/master
Create Date:            2020/6/24
Create Time:            14:58
Description:            override default encoding for open()
Long Description:       override default encoding for open()
                        if encoding is not specified, the encoding used is platform dependent:
                        locale.getpreferredencoding(False) is called to get the current locale encoding.
                        (For reading and writing raw bytes use binary mode and leave encoding unspecified.)

                        if files' encoding does not same with system's encoding(locale.getpreferredencoding())
                            M1: set interpreter options '-X utf8'
                            M2: override locale:
                                `import _locale;_locale._getdefaultlocale = (lambda *args: ['en_US', 'utf8'])`
    backup files and replace string inplace
References:             [gbk所导致的open()函数报错及其他编码问题](https://juejin.im/post/5bd2b6d5e51d45735c3c0453)
                        [UnicodeDecodeError: 'gbk' codec问题解决方案](https://www.codetd.com/article/10353850)
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

import _locale
import locale

if __name__ == '__main__':
    import sys

    print(sys.flags.utf8_mode)
    print(locale.getdefaultlocale())  # on Windows with gbk setting: -> ('zh_CN', 'cp936')
    print(locale.getpreferredencoding())  # on Windows with gbk setting: -> 'cp936'

    # override default locale
    _locale._getdefaultlocale = (lambda *args: ['en_US', 'utf8'])

    print(sys.flags.utf8_mode)  # only can impacted by setting interpreter options '-X utf8', such as 'py -X utf8 x.py'
    print(locale.getdefaultlocale())  # -> ('en_US', 'utf8')
    print(locale.getpreferredencoding())  # -> utf8
