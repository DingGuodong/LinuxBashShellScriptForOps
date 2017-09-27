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
    Example: python %s "admin@example.domain" "Test email from Python" "Python rules them all!"
""") % (__file__, sys.argv[0])
    sys.exit(0)


EMAIL_HOST = "smtp.example.domain"  # change it
EMAIL_PORT = 25  # default smtp port
EMAIL_HOST_USER = 'noreply@example.domain'  # change it
EMAIL_HOST_PASSWORD = 'your password'  # change it
DEFAULT_FROM_EMAIL = 'noreply@example.domain'  # change it, https://tools.ietf.org/html/rfc822.html#appendix-A
CRLF = "\r\n"  # for Windows user read easily

# user defined variable, in Zabbix is {ALERT.SENDTO}
EMAIL_TO = "example@example.domain"
# user defined variable, in Zabbix is {ALERT.SUBJECT}
EMAIL_SUBJECT = "An email notification from Python"
# user defined variable, in Zabbix is {ALERT.MESSAGE}
EMAIL_BODY = "if you saw this content, it means it works and this is default content with no parameters."

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

BODY = string.join((
    "From: %s" % DEFAULT_FROM_EMAIL,
    "To: %s" % EMAIL_TO,
    "Subject: %s" % EMAIL_SUBJECT,
    "",
    EMAIL_BODY
), CRLF)

server = smtplib.SMTP()
server.connect(EMAIL_HOST, EMAIL_PORT)
server.starttls()
server.login(EMAIL_HOST_USER, EMAIL_HOST_PASSWORD)
server.sendmail(DEFAULT_FROM_EMAIL, [EMAIL_TO], BODY)
server.quit()
