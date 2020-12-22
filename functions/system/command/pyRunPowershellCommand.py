#!/usr/bin/python
# encoding: utf-8
# -*- coding: utf-8 -*-
"""
Created by PyCharm.
File Name:              LinuxBashShellScriptForOps:pyRunPowershellCommand.py
Version:                0.0.1
Author:                 Guodong
Author Email:           dgdenterprise@gmail.com
URL:                    https://github.com/DingGuodong/LinuxBashShellScriptForOps
Download URL:           https://github.com/DingGuodong/LinuxBashShellScriptForOps/tarball/master
Create Date:            2019/1/15
Create Time:            13:10
Description:            run Powershell command in Python on Windows
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

import subprocess

from base64 import b64encode


def run_ascii_command():
    ps_command = '(Get-Process lsass).Responding'  # get process responding status on Windows

    command = "powershell.exe " + ps_command
    p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    (stdout, stderr) = p.communicate()

    print(stdout.strip())
    print(stderr.strip())


def to_unicode_or_bust(obj, encoding='utf-8'):
    """
    convert non-unicode object to unicode object
    :param obj: str object or unicode
    :param encoding:
    :return:
    """
    import six
    if six.PY3:
        return obj

    if isinstance(obj, basestring):
        if not isinstance(obj, unicode):
            obj = unicode(obj, encoding)

    return obj


def run_unicode_command():
    """
    when command or script contains chinese characters,
    we should use the -EncodedCommand parameter to avoid encoding issue
    当命令或脚本中包含中文字符时，应该使用-EncodedCommand参数来执行powershell以避免编码（乱码）问题

    must use utf16 little endian(BOM) on windows before base64 encoding
    在base64编码前，在Windows中必须使用utf16 小端节（即BOM）的编码

    gbk is default encoding for Windows Chinese version, so you will see codes like 'decode("gbk")' below
    Windows中文版系统默认使用gbk编码，所以你会在下方看到有gbk解码，具体系统以具体编码为准。

    :return:
    :rtype:
    """
    script = '(NET USER {name} | where {{$_ -match "帐户启用*"}}).Split()|select -Last 1'.format(name="guest")

    script = to_unicode_or_bust(script)
    # -EncodedCommand
    #     接受 base-64 编码字符串版本的命令。使用此参数
    #     向 Windows PowerShell 提交需要复杂引号
    #     或大括号的命令。

    # must use utf16 little endian(BOM) on windows
    # in python3: bytes to str using 'decode("ascii")'
    encoded_ps = b64encode(script.encode('utf_16_le')).decode("ascii")

    command = "powershell.exe -EncodedCommand {0}".format(encoded_ps)

    p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    (stdout, stderr) = p.communicate()

    print(stdout.decode("gbk").strip())
    print(stderr.decode("gbk").strip())


if __name__ == '__main__':
    run_ascii_command()
    run_unicode_command()
