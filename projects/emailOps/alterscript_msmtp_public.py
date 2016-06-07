#!/usr/bin/python
# encoding: utf-8
# -*- coding: utf8 -*-
import smtplib
import string
import sys


def usage():
    print("""
    Function: send email to somebody using smtp protocol

    Usage:
        no parameters:   python %s
        with parameters: python %s <mailto> <subject> <message body>

    Example: python %s "sendto" "subject" "message"
""") % (__file__, __file__, sys.argv[0])
    sys.exit(0)


EMAIL_HOST = "smtp.example.domain"  # change it
EMAIL_PORT = 25  # default smtp port
EMAIL_HOST_USER = 'noreply@example.domain'  # change it
EMAIL_HOST_PASSWORD = 'your password'  # change it
DEFAULT_FROM_EMAIL = 'noreply@example.domain'  # change it
CRLF = "\r\n"  # for Windows user read easily

# user defined variable, in Zabbix is {ALERT.SENDTO}
EMAIL_TO = "example@example.domain"
# user defined variable, in Zabbix is {ALERT.SUBJECT}
SUBJECT = "An email notification from Python"
# user defined variable, in Zabbix is {ALERT.MESSAGE}
text = "if you saw this content, it means it works and this is default content with no parameters."

argc = len(sys.argv)
if not (argc == 1 or argc == 4):
    print("Error: incorrect number of arguments or unrecognized option")
    usage()
if argc == 1:
    pass
else:
    if sys.argv[1] is not None and sys.argv[2] is not None and sys.argv[3] is not None:
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
