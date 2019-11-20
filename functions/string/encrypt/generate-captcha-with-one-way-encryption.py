#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created by PyCharm.
File Name:              LinuxBashShellScriptForOps:generate-captcha-with-one-way-encryption.py
Version:                0.0.1
Author:                 dgden
Author Email:           dgdenterprise@gmail.com
URL:                    https://github.com/DingGuodong/LinuxBashShellScriptForOps
Download URL:           https://github.com/DingGuodong/LinuxBashShellScriptForOps/tarball/master
Create Date:            2019/11/20
Create Time:            11:51
Description:            
Long Description:       
References:             https://tools.ietf.org/html/rfc4226
                        https://tools.ietf.org/html/rfc6238
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
import hashlib
import hmac
import time


def generate_6bits_captcha_using_totp(key='base32secret3232', interval=30):
    msg = str(int(time.time() / interval))
    hmac_sha1 = hmac.new(key=key, msg=msg, digestmod=hashlib.sha1)
    hmac_sha1_digest = hmac_sha1.digest()  # __len__() 20 bit

    digit = 6
    offset = ord(hmac_sha1_digest[19]) & 0xf  # type: int
    bin_code = (ord(hmac_sha1_digest[offset]) & 0x7f) << 24 | \
               (ord(hmac_sha1_digest[offset + 1]) & 0xff) << 16 | \
               (ord(hmac_sha1_digest[offset + 2]) & 0xff) << 8 | \
               (ord(hmac_sha1_digest[offset + 3]) & 0xff)  # type: int
    otp = str(bin_code % 10 ** digit)  # type: str
    while len(otp) < digit:
        otp = '0' + otp

    return otp


if __name__ == '__main__':
    print(generate_6bits_captcha_using_totp())
    time.sleep(1)
    print(generate_6bits_captcha_using_totp())
    time.sleep(29)
    print(generate_6bits_captcha_using_totp())
