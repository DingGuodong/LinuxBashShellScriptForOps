#!/usr/bin/python
# encoding: utf-8
# -*- coding: utf8 -*-
"""
Created by PyCharm.
File Name:              LinuxBashShellScriptForOps:pyRunSystemCommand.py
Version:                0.0.1
Author:                 Guodong
Author Email:           dgdenterprise@gmail.com
URL:                    https://github.com/DingGuodong/LinuxBashShellScriptForOps
Download URL:           https://github.com/DingGuodong/LinuxBashShellScriptForOps/tarball/master
Create Date:            2017/10/17
Create Time:            10:14
Description:            python run some command with option capture stdout or not
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


def run(command, capture_stdout=False, suppress_stdout=False):
    import subprocess

    p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE,
                         stderr=subprocess.STDOUT)
    (stdout, stderr) = p.communicate()

    if p.returncode != 0:  # run command failed
        print "encountered an error (return code %s) while executing '%s'" % (p.returncode, command)
        if stdout is not None:
            print "Standard output:\n", decoding(stdout)
        if stderr is not None:
            print "Standard error:\n", decoding(stderr)
        if not capture_stdout:
            return False
        else:
            return ""
    else:  # run command success

        if stdout is not None:
            if capture_stdout:
                return stdout
            else:
                if not suppress_stdout:
                    print decoding(stdout)
                return True


if __name__ == '__main__':
    run("uname -a")
