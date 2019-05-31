#!/usr/bin/python
# encoding: utf-8
# -*- coding: utf8 -*-
"""
Created by PyCharm.
File:               LinuxBashShellScriptForOps:sendEmailWithSMTP.py
User:               Guodong
Create Date:        2017/5/12
Create Time:        16:59
 """
import smtplib


class sendMailOverSMTP(object):
    def __init__(self):
        self.email = smtplib.SMTP()

    def connect(self, host, port, username, password, tls=True):
        smtp_host = host
        smtp_port = int(port)
        smtp_username = username
        smtp_password = password

        self.email.connect(smtp_host, smtp_port)
        if tls:
            self.email.starttls()
        self.email.login(smtp_username, smtp_password)
        return self.email

    def send(self, from_user, to_user, subject, text):
        CRLF = "\r\n"  # for Windows user

        body = CRLF.join((
            "From: %s" % from_user,
            "To: %s" % to_user,
            "Subject: %s" % subject,
            "",
            text
        ))

        self.email.sendmail(from_user, [to_user], body)
        self.email.quit()


if __name__ == '__main__':
    mail = sendMailOverSMTP()
    mail.connect('smtp.example.domain', 465, 'your_name@example.domain', 'your_password_here', tls=True)
    mail.send('from_who@example.domain', 'to_who@example.domain', 'Subject_here', 'Content_here')
