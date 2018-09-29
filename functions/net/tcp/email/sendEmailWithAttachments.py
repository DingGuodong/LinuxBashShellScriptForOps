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
Updates:                Add Chinese characters support, both of sender, subject, attachments' name
                        can contain no-ascii characters
 """

import os
import smtplib
import time
from email.header import Header
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formatdate, make_msgid


def to_unicode_or_bust(obj, encoding='utf-8'):
    # the function convert non-unicode object to unicode object
    if isinstance(obj, basestring):
        if not isinstance(obj, unicode):
            obj = unicode(obj, encoding)

    return obj


def sendmail(send_from, send_to, subject, text, files=None, cc=None):
    assert isinstance(send_to, list)

    msg = MIMEMultipart()
    msg['From'] = Header(send_from, 'utf-8')
    msg['To'] = ", ".join(send_to)
    msg['Date'] = formatdate(localtime=True)
    msg['Message-ID'] = make_msgid()  # Returns a string suitable for RFC 2822 compliant Message-ID.
    msg['Subject'] = Header(subject, 'utf-8')
    msg.attach(MIMEText(text, 'plain', 'utf-8'))  # MIMEText(html,'html','utf8')

    if cc is not None:
        msg['CC'] = cc

    for attachment in files or []:
        attachment = to_unicode_or_bust(attachment)  # convert str to unicode
        if os.path.exists(attachment):  # Unicode is required
            filename = os.path.basename(attachment)
            with open(attachment, "rb") as fd:  # Unicode is required
                part = MIMEApplication(
                    fd.read(),
                    Name=filename,
                )
            part['Content-Disposition'] = 'attachment; filename="%s"' % filename.encode("utf-8")
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
