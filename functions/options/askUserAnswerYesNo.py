#!/usr/bin/python
# encoding: utf-8
# -*- coding: utf8 -*-
"""
Created by PyCharm.
File:               LinuxBashShellScriptForOps:askUserAnswer.py
User:               Guodong
Create Date:        2016/11/28
Create Time:        21:22
 """

import os


def ask(message, options):
    """
    Ask the message interactively, with the given possible responses
    :parameter message show message for users
    :parameter options y or n
    """
    while 1:
        if os.environ.get('PIP_NO_INPUT'):
            raise Exception(
                'No input was expected ($PIP_NO_INPUT set); question: %s' %
                message
            )
        response = input(message)
        response = response.strip().lower()
        if response not in options:
            print(
                'Your response (%r) was not one of the expected responses: '
                '%s' % (response, ', '.join(options))
            )
        else:
            return response


answer = ask('Proceed (y/n)? ', ('y', 'n'))
if answer == 'y':
    print('y')
else:
    print('n')
