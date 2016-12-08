#!/usr/bin/python
# encoding: utf-8
# -*- coding: utf8 -*-
"""
Created by PyCharm.
File:               LinuxBashShellScriptForOps:pyDesOps.py
User:               Guodong
Create Date:        2016/12/7
Create Time:        22:05
 """
import pyDes
from Crypto.Hash import SHA256  # from pycrypto
from Crypto.Cipher import AES
from Crypto import Random
from Crypto.Random import random

des = pyDes.des('This Key')
print des.encrypt('SomeData').encode('hex')

sha256 = SHA256.new()
sha256.update('message')
print sha256.hexdigest()

obj = AES.new('This is a key123', AES.MODE_CBC, 'This is an IV456')
message = "The answer is no"
ciphertext = obj.encrypt(message).encode('hex')
obj2 = AES.new('This is a key123', AES.MODE_CBC, 'This is an IV456')
plaintext = obj2.decrypt(ciphertext.decode('hex'))
print ciphertext, plaintext

rndfile = Random.new()
print rndfile.read(16).encode('hex')

print random.choice(['dogs', 'cats', 'bears'])
