#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created by PyCharm.
File Name:              LinuxBashShellScriptForOps:py-print-text-with-color-in-console.py
Version:                0.0.1
Author:                 dgden
Author Email:           dgdenterprise@gmail.com
URL:                    https://github.com/DingGuodong/LinuxBashShellScriptForOps
Download URL:           https://github.com/DingGuodong/LinuxBashShellScriptForOps/tarball/master
Create Date:            2019/8/27
Create Time:            10:11
Description:            print text with color in console(such as ssh shell, Linux Terminal, Pycharm IDE)
Long Description:       not support on Microsoft cmd and powershell
References:             from fabric.colors import red, green
Prerequisites:          pip2.7 install fabric==1.14.0
Development Status:     3 - Alpha, 5 - Production/Stable
Environment:            Console
Intended Audience:      System Administrators, Developers, End Users/Desktop
License:                Freeware, Freely Distributable
Natural Language:       English, Chinese (Simplified)
Operating System:       POSIX :: Linux, Microsoft :: Windows
Programming Language:   Python :: 2.6
Programming Language:   Python :: 2.7
Topic:                  Utilities
Tips:                   https://support.microsoft.com/en-us/help/12373/windows-update-faq
                        What is the difference between a feature and quality update?
                        Feature updates are typically include new functionality and capabilities as well as potential
                        fixes and security updates.
                        Quality updates are more frequent and mainly include small fixes and security updates.
 """

import os


def _wrap_with(code):
    def inner(text, bold=False):
        c = code

        if os.environ.get('FABRIC_DISABLE_COLORS'):  # or os.name == 'nt':
            return text

        if bold:
            c = "1;%s" % c
        return "\033[%sm%s\033[0m" % (c, text)

    return inner


red = _wrap_with('31')
green = _wrap_with('32')
yellow = _wrap_with('33')
blue = _wrap_with('34')
magenta = _wrap_with('35')
cyan = _wrap_with('36')
white = _wrap_with('37')

if __name__ == '__main__':
    if os.name == 'nt':
        print("not support on Microsoft cmd and powershell")
    print(red("hello world!"))
    print(green("hello world!"))
    print(yellow("hello world!"))
    print(blue("hello world!"))
    print(magenta("hello world!"))
    print(cyan("hello world!"))
    print(white("hello world!"))
