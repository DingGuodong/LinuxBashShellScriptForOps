#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created by PyCharm.
File Name:              LinuxBashShellScriptForOps:pywin32-win32crypt-quick-example.py
Version:                0.0.1
Author:                 dgden
Author Email:           dgdenterprise@gmail.com
URL:                    https://github.com/DingGuodong/LinuxBashShellScriptForOps
Download URL:           https://github.com/DingGuodong/LinuxBashShellScriptForOps/tarball/master
Create Date:            2019/11/21
Create Time:            16:01
Description:            using win32crypt to encrypt string
Long Description:       useful for password encryption
References:             [CryptProtectData](
                        https://docs.microsoft.com/en-us/windows/win32/api/dpapi/nf-dpapi-cryptprotectdata)
                        [CryptUnprotectData](
                        https://docs.microsoft.com/zh-cn/windows/win32/api/dpapi/nf-dpapi-cryptunprotectdata)
Prerequisites:          pip install pywin32
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
from base64 import b64encode

import win32crypt

pDataIn = "My test data"  # the plaintext to be encrypted.

# A string with a readable description of the data to be encrypted.
# This description string is included with the encrypted data. This parameter is optional and can be set to None.
szDataDescr = "My description"

pOptionalEntropy = None
pvReserved = None
pPromptStruct = None
dwFlags = 0  # CRYPTPROTECT_LOCAL_MACHINE

# https://docs.microsoft.com/en-us/previous-versions/aa922939(v=msdn.10)?redirectedfrom=MSDN#remarks
# Only a user with logon credentials matching those of the encrypter can decrypt the data.
# In addition, decryption usually can only be done on the computer where the data was encrypted.
pDataOut = win32crypt.CryptProtectData(pDataIn, szDataDescr, pOptionalEntropy, pvReserved, pPromptStruct, dwFlags)
print(pDataOut)
print(b64encode(pDataOut))

pDescrOut, pDataOut = win32crypt.CryptUnprotectData(pDataOut, pOptionalEntropy, pvReserved, pPromptStruct, dwFlags)
print(pDescrOut, pDataOut)
