#!/usr/bin/python
# encoding: utf-8
# -*- coding: utf8 -*-
"""
Created by PyCharm.
File Name:              LinuxBashShellScriptForOps:sendEmailWithAttachments.py
Version:                0.0.1
Author:                 Guodong
Author Email:           dgdenterprise@gmail.com
URL:                    https://github.com/DingGuodong/LinuxBashShellScriptForOps
Download URL:           https://github.com/DingGuodong/LinuxBashShellScriptForOps/tarball/master
Create Date:            2017/12/14
Create Time:            11:56
Description:            send email with some files as attachments by smtplib with Python
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

import os
import smtplib
import sys
import time
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate


def usage():
    print("""
    Function: send email to somebody using smtp protocol
    Usage: python %s <mailto> <subject> <message body>
    Zabbix setting: 'Administration' -> 'Media types' 
                    https://hostname/zabbix.php?action=mediatype.edit&mediatypeid=4
                    Script parameters: {ALERT.SENDTO} {ALERT.SUBJECT} {ALERT.MESSAGE}
    Example: python %s "dinggd@example.cn" "Test email from Python" "Python rules them all!"
""") % (__file__, sys.argv[0])
    sys.exit(0)


def sendmail(send_from, send_to, subject, text, files=None):
    assert isinstance(send_to, list)

    msg = MIMEMultipart()
    msg['From'] = send_from
    msg['To'] = COMMASPACE.join(send_to)  # To, Cc, Bcc; Bcc should be used carefully.
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = subject
    msg.attach(MIMEText(text))

    for attachment in files or []:
        if os.path.exists(attachment):
            filename = os.path.basename(attachment)
            with open(attachment, "rb") as fil:
                part = MIMEApplication(
                    fil.read(),
                    Name=filename
                )
            # After the file is closed
            part['Content-Disposition'] = 'attachment; filename="%s"' % filename
            msg.attach(part)

    smtp = smtplib.SMTP()
    smtp.connect(EMAIL_HOST, EMAIL_PORT)
    smtp.starttls()
    smtp.login(EMAIL_HOST_USER, EMAIL_HOST_PASSWORD)
    smtp.sendmail(send_from, send_to, msg.as_string())
    smtp.close()


if __name__ == '__main__':
    TODAY = time.strftime('%Y-%m-%d', time.localtime(time.time()))
    EMAIL_TO = ["xxx@exmaple.com", 'yyy@exmaple.com', 'zzz@example.com']  # object: list
    EMAIL_SUBJECT = "Business service Statistics - {date}".format(date=TODAY)
    EMAIL_BODY = "FYR.\n" \
                 "\n" \
                 "best regards,\n" \
                 "Business Service Statistics Reporter, Ops Team"  # for Windows user use CRLF = "\r\n"
    # user defined variable, email attachments you want add
    EMAIL_ATTACHMENTS = [__file__, ]  # object: list

    EMAIL_HOST = "smtp.example.com"
    EMAIL_PORT = 465
    EMAIL_HOST_USER = 'noreply@exmaple.com'
    EMAIL_HOST_PASSWORD = 'password'
    DEFAULT_FROM_EMAIL = r'"Business Service Statistics Reporter" <noreply@exmaple.com>'

    sendmail(send_from=DEFAULT_FROM_EMAIL, send_to=EMAIL_TO, subject=EMAIL_SUBJECT, text=EMAIL_BODY,
             files=EMAIL_ATTACHMENTS)
