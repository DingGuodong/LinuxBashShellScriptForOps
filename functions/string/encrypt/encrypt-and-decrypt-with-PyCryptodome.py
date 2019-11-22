#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created by PyCharm.
File Name:              LinuxBashShellScriptForOps:encrypt-and-decrypt-with-PyCryptodome.py
Version:                0.0.1
Author:                 dgden
Author Email:           dgdenterprise@gmail.com
URL:                    https://github.com/DingGuodong/LinuxBashShellScriptForOps
Download URL:           https://github.com/DingGuodong/LinuxBashShellScriptForOps/tarball/master
Create Date:            2019/11/22
Create Time:            9:53
Description:            AES and RSA encryption in pycryptodome
Long Description:       
References:             [pycryptodome](https://github.com/Legrandin/pycryptodome)
                        [PyCryptodome’s documentation](https://www.pycryptodome.org/en/latest/)
Prerequisites:          pip install pycryptodome  # if PyCrypto is NOT installed
                        pip install pycryptodomex  # if PyCrypto is installed
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
import json
from base64 import b64encode, b64decode

from Crypto import Random
from Crypto.Cipher import AES, PKCS1_v1_5
from Crypto.Hash import SHA
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad


def encrypt_aes_cbc(data):
    cipher_aes = AES.new(key=aes_key_16b, mode=AES.MODE_CBC)
    ct_bytes = cipher_aes.encrypt(plaintext=pad(data, AES.block_size))
    iv = b64encode(cipher_aes.iv).decode('utf-8')  # Initialization Vector, nonce
    ct = b64encode(ct_bytes).decode('utf-8')
    result = json.dumps({'iv': iv, 'cipher_text': ct})
    return result


def decrypt_aes_cbc(data):
    try:
        b64 = json.loads(data)
        iv = b64decode(b64['iv'])
        ct = b64decode(b64['cipher_text'])
        cipher_aes = AES.new(aes_key_16b, AES.MODE_CBC, iv)
        pt = unpad(cipher_aes.decrypt(ct), AES.block_size)
        return pt
    except (ValueError, KeyError):
        print("Incorrect decryption")


def encrypt_pkcs1_rsa(data):
    key_rsa = RSA.importKey(open('C:/Users/dgden/.ssh/putty_rsa-key-1024-20150918.public.rsa').read())
    h = SHA.new(data)
    cipher_rsa = PKCS1_v1_5.new(key_rsa)
    cipher_text = cipher_rsa.encrypt(data+h.digest())
    return cipher_text


def decrypt_pkcs1_rsa(data):
    key_rsa = RSA.importKey(open('C:/Users/dgden/.ssh/putty_rsa-key-1024-20150918.private.openssh').read())
    dsize = SHA.digest_size
    sentinel = Random.new().read(15+dsize)
    cipher_rsa = PKCS1_v1_5.new(key_rsa)
    message = cipher_rsa.decrypt(data, sentinel)
    digest = SHA.new(message[:-dsize]).digest()
    if digest == message[-dsize:]:
        return message[:-dsize]


if __name__ == '__main__':
    msg = "hello world"  # type: bytes
    aes_key_16b = get_random_bytes(16)

    # AES
    msg_encrypted = encrypt_aes_cbc(msg)
    msg_decrypted = decrypt_aes_cbc(msg_encrypted)
    print(msg_decrypted)
    assert msg == msg_decrypted

    # RSA
    msg_encrypted_rsa = encrypt_pkcs1_rsa(msg)
    msg_decrypted_rsa = decrypt_pkcs1_rsa(msg_encrypted_rsa)
    print(msg_decrypted_rsa)
    assert msg == msg_decrypted_rsa
