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
References:             https://stackoverflow.com/questions/3362600/how-to-send-email-attachments
                        https://stackoverflow.com/a/16509278
                        https://stackoverflow.com/a/50878758

Prerequisites:          []
Development Status:     3 - Alpha, 5 - Production/Stable
Environment:            Console
Intended Audience:      System Administrators, Developers, End Users/Desktop
License:                Freeware, Freely Distributable
Natural Language:       English, Chinese (Simplified)
Operating System:       POSIX :: Linux, Microsoft :: Windows
Programming Language:   Python :: 3
Topic:                  Utilities
Updates:                Add Chinese characters support, both of sender, subject, attachments' name
                        can contain no-ascii characters
 """
import locale
import smtplib
import sys
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formatdate
# from email import encoders
from os.path import basename, exists

import time

encoding = locale.getpreferredencoding()


def usage():
    print("""
    Function: send email to somebody using smtp protocol
    Usage: python %s <mailto> <subject> <message body>
    Zabbix setting: 'Administration' -> 'Media types' 
                    https://hostname/zabbix.php?action=mediatype.edit&mediatypeid=4
                    Script parameters: {ALERT.SENDTO} {ALERT.SUBJECT} {ALERT.MESSAGE}
    Example: python %s "dinggd@e-bao.cn" "Test email from Python" "Python rules them all!"
""") % (__file__, sys.argv[0])
    sys.exit(0)


def send_mail(send_from, send_to, subject, text, files=None, enable_cc=False):
    """Compose and send email with provided info and attachments.

    Args:
        send_from (str): from name
        send_to (list): to name
        subject (str): message title
        text (str): message body
        files (list[str]): list of file paths to be attached to email
        enable_cc (bool): enable cc or not
    """

    msg = MIMEMultipart()
    msg['From'] = send_from
    msg['To'] = ', '.join(send_to)
    if enable_cc:
        msg['To'] = ""
        msg['Cc'] = ";".join(send_to)
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = subject  # Header(subject, 'utf-8')
    msg["Accept-Language"] = "zh-CN, en-US"
    msg["Content-Language"] = "zh-CN"
    msg["Accept-Charset"] = "utf-8"
    msg.set_charset("utf-8")

    # using 'html' to replace 'plain' when email body in html format.
    msg.attach(MIMEText(text, 'plain'))  # 'plain' format can be 'html', but don't set 'base64'

    for attachment in files or []:
        if exists(attachment):
            with open(attachment, "rb") as fp:
                part = MIMEApplication(fp.read())
            # encoders.encode_base64(part)  # encode attachment to base64, Content-Transfer-Encoding: base64
            part.add_header('Content-Disposition', 'attachment', filename=("utf-8", "", basename(attachment)))

            msg.attach(part)

    print(msg)

    smtp = smtplib.SMTP(EMAIL_HOST)
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

    argc = len(sys.argv)
    if not (argc == 1 or argc >= 4):
        print("Error: incorrect number of arguments or unrecognized option")
        usage()
    if argc == 1:
        pass
    else:
        EMAIL_TO = [sys.argv[1], ]
        EMAIL_SUBJECT = sys.argv[2]
        EMAIL_BODY = sys.argv[3]
        if len(sys.argv) > 4:
            EMAIL_ATTACHMENTS = sys.argv[4:]

    send_mail(send_from=DEFAULT_FROM_EMAIL, send_to=EMAIL_TO, subject=EMAIL_SUBJECT, text=EMAIL_BODY,
              files=EMAIL_ATTACHMENTS)
