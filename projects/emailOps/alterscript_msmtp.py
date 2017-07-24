#!/usr/bin/python
# encoding: utf-8
# -*- coding: utf8 -*-
"""
Created by PyCharm.
File:               LinuxBashShellScriptForOps:alterscript_msmtp_v2.py
User:               Guodong
Create Date:        2017/7/24
Create Time:        8:45
Description:        send email using smtplib for zabbix alter script use
References:         https://docs.python.org/2/library/smtplib.html
 """
import smtplib
import string
import sys


def usage():
    print("""
    Function: send email to somebody using smtp protocol
    Usage: python %s <mailto> <subject> <message body>
    Zabbix setting: 'Administration' -> 'Media types' 
                    https://hostname/zabbix.php?action=mediatype.edit&mediatypeid=4
                    Script parameters: {ALERT.SENDTO} {ALERT.SUBJECT} {ALERT.MESSAGE}
    Example: python %s "dinggd@huntor.cn" "Test email from Python" "Python rules them all!"
""") % (__file__, sys.argv[0])
    sys.exit(0)


EMAIL_HOST = "smtp.exmail.qq.com"
EMAIL_PORT = 25
EMAIL_HOST_USER = 'noreply@huntor.cn'
EMAIL_HOST_PASSWORD = 'huntor_nor_123'
DEFAULT_FROM_EMAIL = r'"Zabbix" <noreply@huntor.cn>'  # https://tools.ietf.org/html/rfc822.html#appendix-A
CRLF = "\r\n"  # for Windows user

EMAIL_TO = "dinggd@huntor.cn"  # user defined variable, in Zabbix is {ALERT.SENDTO}
SUBJECT = "Test email from Python"  # user defined variable, in Zabbix is {ALERT.SUBJECT}
text = "Python rules them all!"  # user defined variable, in Zabbix is {ALERT.MESSAGE}

argc = len(sys.argv)
if not (argc == 1 or argc == 4):
    print("Error: incorrect number of arguments or unrecognized option")
    usage()
if argc == 1:
    pass
else:
    if sys.argv[1] != '' and sys.argv[2] != '' and sys.argv[3] != '':
        EMAIL_TO = sys.argv[1]
        SUBJECT = sys.argv[2]
        text = sys.argv[3]

BODY = string.join((
    "From: %s" % DEFAULT_FROM_EMAIL,
    "To: %s" % EMAIL_TO,
    "Subject: %s" % SUBJECT,
    "",
    text
), CRLF)

server = smtplib.SMTP()
server.connect(EMAIL_HOST, EMAIL_PORT)
server.starttls()
server.login(EMAIL_HOST_USER, EMAIL_HOST_PASSWORD)
server.sendmail(DEFAULT_FROM_EMAIL, [EMAIL_TO], BODY)
server.quit()
