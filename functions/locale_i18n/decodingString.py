#!/usr/bin/python
# encoding: utf-8
# -*- coding: utf8 -*-
"""
Created by PyCharm.
File:               LinuxBashShellScriptForOps:decodingString.py
User:               Guodong
Create Date:        2016/12/15
Create Time:        9:43
Notes:              1. what coding you used to decoding string depends on what coding you used to encoding.
                    it is same between encoding and decoding method.
                    2. do not add('+' operator in python syntax) Chinese Language string with a kind of coding
                    to other different coding， such as "u'1' + u'汉字'.encode('gbk')" or "u'1' + '汉字'.encode('utf8')"
                    3. import wmi; print wmi.WMI().Win32_OperatingSystem()[0].MUILanguages
                    4. PowerShell: [System.Text.Encoding]::Default.EncodingName
                    get: 简体中文(GB2312)
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
    import sys

    mswindows = (sys.platform == "win32")

    p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE,
                         stderr=subprocess.STDOUT)
    (stdout, stderr) = p.communicate()

    if p.returncode != 0:
        print "encountered an error (return code %s) while executing '%s'" % (p.returncode, command)
        if stdout is not None:
            if mswindows:
                try:
                    print "Standard output: " + stdout.decode(DEFAULT_LOCALE_ENCODING)
                except UnicodeDecodeError:
                    print "Standard output: " + stdout
            else:
                print "Standard output: " + stdout
        if stderr is not None:
            if mswindows:
                try:
                    print "Standard error: " + stderr.decode(DEFAULT_LOCALE_ENCODING)
                except UnicodeDecodeError:
                    print "Standard error: " + stderr
            else:
                print "Standard error: " + stderr

        return False
    else:
        if stdout is not None:
            if mswindows:
                try:
                    print "Standard output: " + stdout.decode(DEFAULT_LOCALE_ENCODING)
                except UnicodeDecodeError:
                    print "Standard output: " + stdout
            else:
                print stdout
        return True


if __name__ == '__main__':
    import commands

    print "current default encoding is: " + DEFAULT_LOCALE_ENCODING + " (cp936 is included in gbk)"
    status, output = commands.getstatusoutput('ls')  # NB This only works (and is only relevant) for UNIX.
    print status, output.decode(DEFAULT_LOCALE_ENCODING)

    run('dir C:\Users\Guodong\Desktop')  # dir returns system default coding 'gbk'

    run('ls C:\Users\Guodong\Desktop')  # 'ls' comes from git-bash(Git For Windows), ls returns 'utf-8'

    print u"1 ", decoding(u'中国汉字ABC123'.encode('gbk'))
    print u"2 ", decoding(u'中国汉字ABC123'.encode('utf-8'))
    print u"3 ", decoding(u'中国汉字ABC123')
