#!/usr/bin/python
# encoding: utf-8
# -*- coding: utf8 -*-
"""
Created by PyCharm.
File:               LinuxBashShellScriptForOps:getReturnCode.py
User:               Guodong
Create Date:        2016/12/13
Create Time:        15:28
 """


def get_system_encoding():
    """
    The encoding of the default system locale but falls back to the given
    fallback encoding if the encoding is unsupported by python or could
    not be determined.  See tickets #10335 and #5846
    """
    import codecs
    import locale
    import sys
    mswindows = (sys.platform == "win32")
    try:
        encoding = locale.getdefaultlocale()[1] or ('ascii' if not mswindows else 'gbk')
        codecs.lookup(encoding)
    except Exception as e:
        del e
        encoding = 'ascii' if not mswindows else 'gbk'  # 'gbk' is Windows default encoding in Chinese language 'zh-CN'
    return encoding


DEFAULT_LOCALE_ENCODING = get_system_encoding()


def decoding(text):
    import sys

    mswindows = (sys.platform == "win32")

    msg = text
    if mswindows:
        try:
            msg = text.decode(DEFAULT_LOCALE_ENCODING)
            return msg
        except (UnicodeDecodeError, UnicodeEncodeError):
            pass
    return msg


def run(command):
    import subprocess

    p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE,
                         stderr=subprocess.STDOUT)
    (stdout, stderr) = p.communicate()

    if p.returncode != 0:
        print "encountered an error (return code %s) while executing '%s'" % (p.returncode, command)
        if stdout is not None:
            print "Standard output:", decoding(stdout)
        if stderr is not None:
            print "Standard error:", decoding(stderr)

        return False
    else:
        if stdout is not None:
            print decoding(stdout)
        return True


if __name__ == '__main__':
    import os

    home = os.path.expanduser('~')  # both Windows and Linux is works. see also, os.devnull
    run('ls {linux_home} || dir {windows_home}'.format(linux_home=home, windows_home=home))
