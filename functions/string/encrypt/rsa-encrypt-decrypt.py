#!/usr/bin/python
# encoding: utf-8
# -*- coding: utf-8 -*-
"""
Created by PyCharm.
File Name:              LinuxBashShellScriptForOps:rsa-encrypt-decrypt.py
Version:                0.0.2
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
import codecs
import os

import rsa


def gen_rsa_key():
    print("generating rsa key pairs, it will take some long time, please keep waiting.")
    pub_key, priv_key = rsa.newkeys(4096)
    with open(public_key_file, 'w') as fp:
        fp.write(pub_key.save_pkcs1().decode("utf-8"))

    with open(private_key_file, 'w') as fp:
        fp.write(priv_key.save_pkcs1().decode("utf-8"))


def check_keys():
    if not all(map(os.path.exists, [private_key_file, public_key_file])):
        gen_rsa_key()


def load_keys():
    check_keys()

    with open(public_key_file, 'r') as fp:
        pub_key = fp.read().encode("utf-8")

    with open(private_key_file, 'r') as fp:
        priv_key = fp.read().encode("utf-8")

    # pub_key = rsa.PublicKey.load_pkcs1_openssl_pem(pub_key)  # for openssl public key
    pub_key = rsa.PublicKey.load_pkcs1(pub_key)
    priv_key = rsa.PrivateKey.load_pkcs1(priv_key)

    return pub_key, priv_key


if __name__ == '__main__':
    private_key_file = "rsa_4096_private.pem"
    public_key_file = "rsa_4096_public.pem"

    cur_pub_key, cur_priv_key = load_keys()

    message = "hello".encode("utf-8")

    crypto = rsa.encrypt(message, cur_pub_key)
    message_decrypted = rsa.decrypt(crypto, cur_priv_key)
    print(message == message_decrypted)

    hash_method = 'SHA-512'
    signature = rsa.sign(message, cur_priv_key, hash_method)  # type: bytes
    print(codecs.encode(signature, 'hex'))

    try:
        rsa.verify(message, signature, cur_pub_key)
    except rsa.pkcs1.VerificationError:
        print('Verification failed')
    else:
        print('Verification succeed')
