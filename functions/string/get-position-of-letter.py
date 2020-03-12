#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created by PyCharm.
File Name:              LinuxBashShellScriptForOps:get-position-of-letter.py
Version:                0.0.1
Author:                 dgden
Author Email:           dgdenterprise@gmail.com
URL:                    https://github.com/DingGuodong/LinuxBashShellScriptForOps
Download URL:           https://github.com/DingGuodong/LinuxBashShellScriptForOps/tarball/master
Create Date:            2020/3/12
Create Time:            9:23
Description:            get position of the letter
Long Description:       
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

from string import lowercase, uppercase


def get_position(letter):
    # type: (str) -> str
    letter_lowercase = letter.strip().lower()
    res = list()
    if len(letter) > 1:
        for single_letter in letter_lowercase:
            try:
                pos = lowercase.index(single_letter) + 1
            except ValueError:
                return "error: bad letter \'{letter}\' in \'{para}\'".format(letter=single_letter, para=letter)
            single_res = "{letter}: {pos}".format(letter=single_letter, pos=pos)
            res.append(single_res)
        return "\n".join(res)
    else:
        try:
            pos = lowercase.index(letter_lowercase) + 1
        except ValueError:
            return "error: bad letter \'{letter}\'".format(letter=letter)
        return "{letter}: {pos}".format(letter=letter, pos=pos)


def print_letters_table():
    import prettytable
    table = prettytable.PrettyTable(border=True, header=True, left_padding_width=0, padding_width=0)
    table.field_names = uppercase
    table.add_row(range(1, len(uppercase) + 1))
    print(table)


if __name__ == '__main__':
    print_letters_table()
    while 1:
        user_input = raw_input("please input the letter you want: ")
        position = get_position(user_input)
        print(position)
