#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created by PyCharm.
File Name:              LinuxBashShellScriptForOps:run-powershell-script-via-winrm.py
Version:                0.0.1
Author:                 dgden
Author Email:           dgdenterprise@gmail.com
URL:                    https://github.com/DingGuodong/LinuxBashShellScriptForOps
Download URL:           https://github.com/DingGuodong/LinuxBashShellScriptForOps/tarball/master
Create Date:            2020/12/23
Create Time:            11:33
Description:            run powershell script via WinRM
Long Description:       execute remote command on Windows, include cmd.exe or powershell

Enable-PSRemoting -Force
set firewall policy for TCP port 5985

References:             [pywinrm](https://github.com/diyan/pywinrm)
Prerequisites:          pip install -U pywinrm
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
import winrm
from base64 import b64encode
from winrm.protocol import Protocol


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


def run_powershell_with_codepage_936(target, username, password, script):
    """
    run remote command with WinRM if your code ran into a garbage text or Chinese characters are not displayed properly

    [Chinese characters are not displayed properly #288](https://github.com/diyan/pywinrm/issues/288)
    [Code Page Identifiers](https://docs.microsoft.com/en-us/windows/win32/intl/code-page-identifiers)

    codepage use 936, gb2312, ANSI/OEM Simplified Chinese (PRC, Singapore); Chinese Simplified (GB2312)

    :param target: hostname or ip address
    :type target: str
    :param username:
    :type username: str
    :param password:
    :type password: str
    :param script: powershell commands or scripts
    :type script: str | unicode
    :return: status_code, std_out
    :rtype: tuple
    """
    script = to_unicode_or_bust(script)
    encoded_ps = b64encode(script.encode('utf_16_le')).decode("ascii")

    p = Protocol(
        endpoint='http://{}:5985/wsman'.format(target),
        transport='ntlm',
        username=username,
        password=password)

    shell_id = p.open_shell(codepage=936)
    try:
        command_id = p.run_command(shell_id, 'powershell.exe', ['-EncodedCommand', encoded_ps])
        try:
            std_out, std_err, status_code = p.get_command_output(shell_id, command_id)
        finally:
            p.cleanup_command(shell_id, command_id)
    finally:
        p.close_shell(shell_id)

    # print(std_out.decode('utf-8'))
    # print(std_err.decode('utf-8'))
    # print(status_code)

    return status_code, std_out, std_err


def run_powershell(target, username, password, script):
    """
    run remote command with WinRM
    :param target: hostname or ip address
    :type target: str
    :param username:
    :type username: str
    :param password:
    :type password: str
    :param script: powershell commands or scripts
    :type script: str | unicode
    :return: status_code, std_out
    :rtype: tuple
    """
    shell = winrm.Session(target, auth=(username, password), transport="ntlm")

    script = to_unicode_or_bust(script)  # python2 using unicode here
    rs = shell.run_ps(script)
    # print rs.status_code, rs.std_out, rs.std_err
    return rs.status_code, rs.std_out, rs.std_err
