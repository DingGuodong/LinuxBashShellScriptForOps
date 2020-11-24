#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created by PyCharm.
File Name:              LinuxBashShellScriptForOps:python-control-outlook-emails.py
Version:                0.0.1
Author:                 dgden
Author Email:           dgdenterprise@gmail.com
URL:                    https://github.com/DingGuodong/LinuxBashShellScriptForOps
Download URL:           https://github.com/DingGuodong/LinuxBashShellScriptForOps/tarball/master
Create Date:            2020/11/24
Create Time:            15:35
Description:            get mail message content from Microsoft Outlook
Long Description:       python win32com outlook
References:             
Prerequisites:          []
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

import pywintypes
import win32com.client

outlook = win32com.client.Dispatch("Outlook.Application").GetNamespace("MAPI")
selected_account = "username@example.com"
selected_folder_name = u'收件箱'

for index in range(10):  # suppose there are 10 mail accounts
    try:
        root_folder = outlook.Folders.Item(index + 1)
        if root_folder.Name == selected_account:
            for item in root_folder.Folders:
                if item.Name == selected_folder_name:
                    messages = item.Items
                    message = messages.GetFirst()

                    while message:
                        try:
                            the_message = dict()
                            the_message["Subject"] = getattr(message, "Subject", "<UNKNOWN>")
                            the_message["SentOn"] = getattr(message, "SentOn", "<UNKNOWN>")
                            the_message["EntryID"] = getattr(message, "EntryID", "<UNKNOWN>")
                            the_message["Sender"] = getattr(message, "Sender", "<UNKNOWN>")
                            # print(the_message["Sender"].Name, the_message["Sender"].Address)

                            the_message["Size"] = getattr(message, "Size", "<UNKNOWN>")
                            the_message["Body"] = getattr(message, "Body", "<UNKNOWN>")
                            print(the_message)
                        except Exception as ex:
                            print("Error processing mail", ex)

                        message = messages.GetNext()

    except pywintypes.com_error:
        pass
