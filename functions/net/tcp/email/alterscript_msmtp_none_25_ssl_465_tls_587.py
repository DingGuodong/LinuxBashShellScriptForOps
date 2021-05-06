#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created by PyCharm.
File Name:              LinuxBashShellScriptForOps:alterscript_msmtp_none_25_ssl_465_tls_587.py.py
Version:                0.0.1
Author:                 dgden
Author Email:           dgdenterprise@gmail.com
URL:                    https://github.com/DingGuodong/LinuxBashShellScriptForOps
Download URL:           https://github.com/DingGuodong/LinuxBashShellScriptForOps/tarball/master
Create Date:            2019/12/18
Create Time:            16:13
Description:            send email using smtplib for zabbix alter script use which support SSL and TLS and None
Long Description:       
References:             https://docs.python.org/2/library/smtplib.html
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
import smtplib
import string
import sys

import six


def usage():
    print("""
    Function: send email to somebody using smtp protocol
    Usage: python %s <mailto> <subject> <message body>
    Zabbix setting: 'Administration' -> 'Media types' 
                    https://hostname/zabbix.php?action=mediatype.edit&mediatypeid=4
                    Script parameters: {ALERT.SENDTO} {ALERT.SUBJECT} {ALERT.MESSAGE}
    Example: python %s "admin@example.domain" "Test email from Python" "Python rules them all!"
""" % (__file__, sys.argv[0]))
    sys.exit(0)


EMAIL_HOST = "smtp.mxhichina.com"
EMAIL_PORT = 25  # default smtp port
EMAIL_HOST_USER = 'sender@example.com'
EMAIL_HOST_PASSWORD = 'password'
EMAIL_HOST_ENABLE_SSL = True
EMAIL_HOST_ENABLE_TLS = False

if EMAIL_HOST_ENABLE_SSL and EMAIL_HOST_ENABLE_TLS:
    raise Exception("can NOT be used together")

if EMAIL_HOST_ENABLE_SSL:
    EMAIL_PORT = 465

DEFAULT_FROM_EMAIL = EMAIL_HOST_USER  # https://tools.ietf.org/html/rfc822.html#appendix-A
CRLF = "\r\n"  # for Windows user

EMAIL_TO = "receiver@example.com"  # user defined variable, in Zabbix is {ALERT.SENDTO}
EMAIL_SUBJECT = "Test email from Python"  # user defined variable, in Zabbix is {ALERT.SUBJECT}
EMAIL_BODY = "Python rules them all!"  # user defined variable, in Zabbix is {ALERT.MESSAGE}

argc = len(sys.argv)
if not (argc == 1 or argc == 4):
    print("Error: incorrect number of arguments or unrecognized option")
    usage()
if argc == 1:
    pass
else:
    if sys.argv[1] != '' and sys.argv[2] != '' and sys.argv[3] != '':
        EMAIL_TO = sys.argv[1]
        EMAIL_SUBJECT = sys.argv[2]
        EMAIL_BODY = sys.argv[3]

if six.PY2:
    BODY = string.join((
        "From: %s" % DEFAULT_FROM_EMAIL,
        "To: %s" % EMAIL_TO,
        "Subject: %s" % EMAIL_SUBJECT,
        "",
        EMAIL_BODY
    ), CRLF)
else:
    BODY = CRLF.join((
        "From: %s" % DEFAULT_FROM_EMAIL,
        "To: %s" % EMAIL_TO,
        "Subject: %s" % EMAIL_SUBJECT,
        "",
        EMAIL_BODY
    ))

if EMAIL_HOST_ENABLE_SSL or EMAIL_HOST_ENABLE_TLS:
    if six.PY3:
        # for python3, ValueError: server_hostname cannot be an empty string or start with a leading dot.
        server = smtplib.SMTP_SSL(host=EMAIL_HOST)
    else:
        server = smtplib.SMTP_SSL()
else:
    server = smtplib.SMTP()

server.connect(EMAIL_HOST, EMAIL_PORT)

if EMAIL_HOST_ENABLE_TLS:
    server.starttls()

server.login(EMAIL_HOST_USER, EMAIL_HOST_PASSWORD)
server.sendmail(DEFAULT_FROM_EMAIL, [EMAIL_TO], BODY)
server.quit()
