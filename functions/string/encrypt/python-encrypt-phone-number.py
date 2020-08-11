#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created by PyCharm.
File Name:              LinuxBashShellScriptForOps:python-encrypt-phone-number.py
Version:                0.0.1
Author:                 dgden
Author Email:           dgdenterprise@gmail.com
URL:                    https://github.com/DingGuodong/LinuxBashShellScriptForOps
Download URL:           https://github.com/DingGuodong/LinuxBashShellScriptForOps/tarball/master
Create Date:            2020/8/11
Create Time:            10:54
Description:            encrypt and decrypt a phone number using AES
Long Description:       
References:             
Prerequisites:          pip install pycrypto
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

import base64
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad


class AesCryptor(object):
    def __init__(self, key):
        self.key = key  # len: any
        self.iv = b'\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0'  # len: 16
        self.aes_mode = AES.MODE_CBC  # AES.MODE_CFB, AES.MODE_CBC, AES.MODE_GCM,

    @staticmethod
    def pkcs7_padding(data):
        return pad(data, AES.block_size)

    @staticmethod
    def pkcs7_unpad(data):
        return unpad(data, AES.block_size)

    def encrypt(self, data):
        data = self.pkcs7_padding(data)
        aes_key = hashlib.sha256(self.key).digest()  # len: 32
        cipher = AES.new(aes_key, self.aes_mode, self.iv)
        encrypted = cipher.encrypt(data)
        return base64.b64encode(encrypted), encrypted.encode('hex')

    def decrypt(self, data):
        data = data.decode('hex')
        aes_key = hashlib.sha256(self.key).digest()  # len: 32
        cipher = AES.new(aes_key, self.aes_mode, self.iv)
        decrypted = cipher.decrypt(data)
        decrypted = self.pkcs7_unpad(decrypted)
        return decrypted


if __name__ == '__main__':
    aes = AesCryptor(key='password')
    encrypted_text = aes.encrypt('18311111111')
    print(encrypted_text)
    plain_text = aes.decrypt(encrypted_text[1])
    print(plain_text)
