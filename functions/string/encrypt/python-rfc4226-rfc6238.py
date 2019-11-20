#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created by PyCharm.
File Name:              LinuxBashShellScriptForOps:python-rfc4226-rfc6238.py
Version:                0.0.1
Author:                 dgden
Author Email:           dgdenterprise@gmail.com
URL:                    https://github.com/DingGuodong/LinuxBashShellScriptForOps
Download URL:           https://github.com/DingGuodong/LinuxBashShellScriptForOps/tarball/master
Create Date:            2019/11/20
Create Time:            14:55
Description:            Python One-Time Password like Google Authenticator
Long Description:       two-step verification
                        Two-Factor Authentication
                        Two-Factor App
References:             https://pyotp.readthedocs.io/en/latest/
                        https://tools.ietf.org/html/rfc4226
                        https://tools.ietf.org/html/rfc6238
Prerequisites:          pip install pyotp
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
import time

import pyotp


def time_based_otp():
    totp = pyotp.TOTP('base32secret3232')
    totp.now()  # => '492039'

    # OTP verified for current time
    totp.verify('492039')  # => True
    time.sleep(30)
    totp.verify('492039')  # => False


def counter_based_otp():
    hotp = pyotp.HOTP('base32secret3232')
    hotp.at(0)  # => '260182'
    hotp.at(1)  # => '055283'
    hotp.at(1401)  # => '316439'

    # OTP verified with a counter
    hotp.verify('316439', 1401)  # => True
    hotp.verify('316439', 1402)  # => False


def generate_base32_secret_key():
    # returns a 16 character base32 secret. Compatible with Google Authenticator and other OTP apps
    print(pyotp.random_base32())


def google_authenticator_compatible():
    print(pyotp.totp.TOTP('JBSWY3DPEHPK3PXP').provisioning_uri("alice@google.com", issuer_name="Secure App"))
    print(pyotp.hotp.HOTP('JBSWY3DPEHPK3PXP').provisioning_uri("alice@google.com", initial_count=0,
                                                               issuer_name="Secure App"))
