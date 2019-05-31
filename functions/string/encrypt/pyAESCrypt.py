#!/usr/bin/python
# encoding: utf-8
# -*- coding: utf-8 -*-
"""
Created by PyCharm.
File Name:              LinuxBashShellScriptForOps:pyAESCrypt.py
Version:                0.0.1
Author:                 Guodong
Author Email:           dgdenterprise@gmail.com
URL:                    https://github.com/DingGuodong/LinuxBashShellScriptForOps
Download URL:           https://github.com/DingGuodong/LinuxBashShellScriptForOps/tarball/master
Create Date:            2019/1/8
Create Time:            14:38
Description:            using AES to encrypt or decrypt with a given password as AES key
Long Description:       
References:             https://github.com/shadowsocks/shadowsocks/blob/master/shadowsocks/cryptor.py
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
from Crypto import Random
from Crypto.Cipher import AES
from Crypto.Hash import MD5

cached_keys = dict()


def EVP_BytesToKey(password, key_len, iv_len):
    """
    With the md5 encryption algorithm, each password has a unique key and iv corresponding to it

    learn from shadowsocks.cryptor.EVP_BytesToKey
    https://github.com/shadowsocks/shadowsocks/blob/master/shadowsocks/cryptor.py
    https://wiki.openssl.org/index.php/EVP
    :param password:
    :param key_len: AES key length: key_size = (16, 24, 32)
    :param iv_len:
    :return:
    """
    # equivalent to OpenSSL's EVP_BytesToKey() with count 1
    # so that we make the same key and iv as nodejs version
    cached_key = '%s-%d-%d' % (password, key_len, iv_len)
    r = cached_keys.get(cached_key, None)
    if r:
        return r
    m = []
    i = 0
    while len(b''.join(m)) < (key_len + iv_len):
        md5 = MD5.new()  # can be replaced with `hashlib.md5()`
        data = password
        if i > 0:
            data = m[i - 1] + password
        md5.update(data)
        m.append(md5.digest())
        i += 1
    ms = b''.join(m)
    key = ms[:key_len]
    iv = ms[key_len:key_len + iv_len]
    cached_keys[cached_key] = (key, iv)
    return key, iv


def generate_aes_256_key_iv(passwd):
    """
    AES key length must be in (16, 24, 32)
    IV length (it must be 16 bytes long)
    :param passwd:
    :return:
    """
    return EVP_BytesToKey(passwd, 32, 16)


def encrypt_aes_256_cfb(key, iv, plaintext, mode=AES.MODE_CFB):
    cfb = AES.new(key, mode, iv)
    return cfb.encrypt(plaintext)


def decrypt_aes_256_cfb(key, iv, plaintext, mode=AES.MODE_CFB):
    cfb = AES.new(key, mode, iv)
    return cfb.decrypt(plaintext)


if __name__ == '__main__':
    rnd = Random.new()
    msg = "hello: " + rnd.read(16).encode("hex")  # make msg human readable

    aes_key, aes_iv = generate_aes_256_key_iv(msg)

    print(aes_key.encode('hex'))
    print(aes_iv.encode('hex'))
    print(len(aes_key + aes_iv))

    secured_msg = encrypt_aes_256_cfb(aes_key, aes_iv, msg)
    plain_msg = decrypt_aes_256_cfb(aes_key, aes_iv, secured_msg)

    print(msg)
    print(plain_msg)
    assert msg == plain_msg
