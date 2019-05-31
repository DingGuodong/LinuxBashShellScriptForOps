#!/usr/bin/python
# encoding: utf-8
# -*- coding: utf8 -*-
"""
Created by PyCharm.
File Name:              LinuxBashShellScriptForOps:pyEncryptDecryptExample.py
Version:                0.0.1
Author:                 Guodong
Author Email:           dgdenterprise@gmail.com
URL:                    https://github.com/DingGuodong/LinuxBashShellScriptForOps
Download URL:           https://github.com/DingGuodong/LinuxBashShellScriptForOps/tarball/master
Create Date:            2018/3/29
Create Time:            16:03
Description:            python encrypt and decrypt data, signature and validate signature
Long Description:       
References:             http://www.jb51.net/article/86022.htm
Prerequisites:          pip install pycrypto
Development Status:     3 - Alpha, 5 - Production/Stable
Environment:            Console
Intended Audience:      System Administrators, Developers, End Users/Desktop
License:                Freeware, Freely Distributable
Natural Language:       English, Chinese (Simplified)
Operating System:       POSIX :: Linux, Microsoft :: Windows
Programming Language:   Python :: 3

Topic:                  Utilities
 """
import base64
import os
import time

from Crypto import Random
from Crypto.Cipher import PKCS1_v1_5 as Cipher_pkcs1_v1_5
from Crypto.Hash import SHA
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5 as Signature_pkcs1_v1_5


def gen_keys():
    print("generate keys ...")
    # generate master private and public keys
    rsa = RSA.generate(4096, random_generator)
    private_pem = rsa.exportKey()
    print(("master private keys: %s" % master_private_key_file))
    with open(master_private_key_file, 'w') as f:
        f.write(private_pem)

    print(("master public keys: %s" % master_public_key_file))
    public_pem = rsa.publickey().exportKey()
    with open(master_public_key_file, 'w') as f:
        f.write(public_pem)

    # generate ghost private and public keys
    rsa = RSA.generate(4096, random_generator)
    private_pem = rsa.exportKey()
    print(("ghost private keys: %s" % ghost_private_key_file))
    with open(ghost_private_key_file, 'w') as f:
        f.write(private_pem)

    print(("ghost public keys: %s" % ghost_public_key_file))
    public_pem = rsa.publickey().exportKey()
    with open(ghost_public_key_file, 'w') as f:
        f.write(public_pem)


def master_encrypt_data(message):
    """
    master peer encrypt data
    :param message:
    :return:
    """
    with open(ghost_public_key_file) as f:
        key = f.read()
        rsa_key = RSA.importKey(key)
        cipher = Cipher_pkcs1_v1_5.new(rsa_key)
        cipher_text = base64.b64encode(cipher.encrypt(message))

        with open(secure_message_file, 'w') as f:
            f.write(cipher_text)


def ghost_decrypt_data_from_file_master_sent(path):
    """
    ghost peer decrypt the encrypted data from a file which master peer generated
    :param path:
    :return: plain text from master peer sent
    """
    with open(path, 'r') as f:
        encrypt_text = f.read()
    with open(ghost_private_key_file) as f:
        key = f.read()
        rsa_key = RSA.importKey(key)
        cipher = Cipher_pkcs1_v1_5.new(rsa_key)
        text = cipher.decrypt(base64.b64decode(encrypt_text), random_generator)
    return text


def signature_message(message):
    """
    master peer signature the encrypted data file
    :param message:
    :return:
    """
    with open(message, 'r') as f:
        message = f.read()
    with open(master_private_key_file, 'r') as f:
        key = f.read()
        rsa_key = RSA.importKey(key)
        signer = Signature_pkcs1_v1_5.new(rsa_key)
        digest = SHA.new()
        digest.update(message)
        sign = signer.sign(digest)
        signature = base64.b64encode(sign)
    with open(secure_message_signature_file, 'w') as f:
        f.write(signature)


def validate_signature(message, signature):
    """
    ghost peer validate the signature with encrypted data file and signature file
    :param message: the encrypted data file
    :param signature: the file contains signature
    :return: boolean type
    """
    with open(message, 'r') as f:
        message = f.read()
    with open(signature, 'r') as f:
        signature = f.read()
    with open(master_public_key_file, 'r') as f:
        key = f.read()
        rsa_key = RSA.importKey(key)
        verifier = Signature_pkcs1_v1_5.new(rsa_key)
        digest = SHA.new()
        digest.update(message)
        is_verify = verifier.verify(digest, base64.b64decode(signature))
        return is_verify


if __name__ == '__main__':
    # define random number generator, this will be used when generate keys
    random_generator = Random.new().read

    # define RSA key path, './.*.pem'
    master_private_key_file = "master-private.pem"
    master_public_key_file = "master-public.pem"
    ghost_private_key_file = "ghost-private.pem"
    ghost_public_key_file = "ghost-public.pem"

    # if pem files not generated, then generate them
    sequence = [
        master_private_key_file,
        master_public_key_file,
        ghost_private_key_file,
        ghost_public_key_file
    ]

    if not all(map(os.path.exists, sequence)):  # itertools.imap() ?
        gen_keys()

    # assume data is exchanged by those files
    secure_message_file = "data_from_master.txt"
    secure_message_signature_file = "data_from_master_signature.txt"

    text_send = "hello, ghost. from master"  # plaintext master peer sent
    print(("Send: %s" % text_send))
    master_encrypt_data(text_send)  # master send encrypted data
    signature_message(secure_message_file)  # master send signature
    time.sleep(2)
    result = ghost_decrypt_data_from_file_master_sent(secure_message_file)  # ghost peer decrypt the encrypted data
    assert text_send == result, 'decrypt failed'
    print(("Get: %s" % result))
    print("Status: encrypt and decrypt is ok")

    if validate_signature(secure_message_file, secure_message_signature_file):  # ghost peer validate signature
        print("Valid signature")
    else:
        print("Invalid signature")
