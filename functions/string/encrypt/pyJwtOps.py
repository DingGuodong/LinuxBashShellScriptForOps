#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created by PyCharm.
File Name:              LinuxBashShellScriptForOps:pyJwtOps.py
Version:                0.0.1
Author:                 dgden
Author Email:           dgdenterprise@gmail.com
URL:                    https://github.com/DingGuodong/LinuxBashShellScriptForOps
Download URL:           https://github.com/DingGuodong/LinuxBashShellScriptForOps/tarball/master
Create Date:            2019/9/10
Create Time:            10:14
Description:            pyJWT code snippets
Long Description:       PyJWT is a Python library which allows you to encode and decode JSON Web Tokens (JWT).
                        JWT is an open, industry-standard (RFC 7519) for
                        representing claims securely between two parties.
References:             https://pyjwt.readthedocs.io/en/latest/
                        https://pyjwt.readthedocs.io/en/latest/usage.html
Prerequisites:          pip install pyjwt
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
import datetime

import jwt

payload = {
    'some': 'payload',
    'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)  # “exp” (Expiration Time) Claim
}

secret = 'secret'

encoded_jwt = ''
try:
    encoded_jwt = jwt.encode(payload, secret, algorithm='HS256')
except jwt.ExpiredSignatureError:
    print("Signature has expired")

decoded_jwt = jwt.decode(encoded_jwt, secret, algorithms='HS256')

print(encoded_jwt)
print(jwt.get_unverified_header(encoded_jwt))
assert payload == decoded_jwt
