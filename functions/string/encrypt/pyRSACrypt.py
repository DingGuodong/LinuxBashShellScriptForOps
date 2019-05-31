#!/usr/bin/python
# encoding: utf-8
# -*- coding: utf-8 -*-
"""
Created by PyCharm.
File Name:              LinuxBashShellScriptForOps:pyRSACrypt.py
Version:                0.0.1
Author:                 Guodong
Author Email:           dgdenterprise@gmail.com
URL:                    https://github.com/DingGuodong/LinuxBashShellScriptForOps
Download URL:           https://github.com/DingGuodong/LinuxBashShellScriptForOps/tarball/master
Create Date:            2018/11/16
Create Time:            15:19
Description:            using RSA to encrypt or decrypt AES or DES keys
Long Description:       
References:             
Prerequisites:          []
Development Status:     3 - Alpha, 5 - Production/Stable
Environment:            Console
Intended Audience:      System Administrators, Developers, End Users/Desktop
License:                Freeware, Freely Distributable
Natural Language:       English, Chinese (Simplified)
Operating System:       POSIX :: Linux, Microsoft :: Windows
Programming Language:   Python :: 3

Topic:                  Utilities
 """
import os


import rsa


def gen_rsa_key():
    print("generating rsa key pairs, it will take some long time, please keep waiting.")
    PublicKey, PrivateKey = rsa.newkeys(4096)
    with open(public_key_file, 'w') as fp:
        fp.write(PublicKey.save_pkcs1())

    with open(private_key_file, 'w') as fp:
        fp.write(PrivateKey.save_pkcs1())


def check_keys():
    if not all(map(os.path.exists, [private_key_file, public_key_file])):
        gen_rsa_key()


def load_keys():
    check_keys()

    with open(public_key_file, 'r') as fp:
        public_key = fp.read()

    with open(private_key_file, 'r') as fp:
        private_key = fp.read()

    PublicKey = rsa.PublicKey.load_pkcs1(public_key)
    PrivateKey = rsa.PrivateKey.load_pkcs1(private_key)

    return PublicKey, PrivateKey


if __name__ == '__main__':
    private_key_file = "rsa_4096_private.pem"
    public_key_file = "rsa_4096_public.pem"

    pub_key, priv_key = load_keys()

    message = "hello"

    crypto = rsa.encrypt(message, pub_key)
    message_decrypted = rsa.decrypt(crypto, priv_key)
    print(message == message_decrypted)

    hash_method = 'SHA-512'
    signature = rsa.sign(message, priv_key, hash_method)
    print(signature.encode('hex'))

    try:
        rsa.verify(message, signature, pub_key)
    except rsa.pkcs1.VerificationError:
        print('Verification failed')
    else:
        print('Verification succeed')
