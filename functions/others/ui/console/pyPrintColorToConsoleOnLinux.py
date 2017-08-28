#!/usr/bin/python
# encoding: utf-8
# -*- coding: utf8 -*-
"""
Created by PyCharm.
File:               LinuxBashShellScriptForOps:pyPrintColorToConsoleOnLinux.py
User:               Guodong
Create Date:        2017/8/28
Create Time:        11:31
Description:        
References:         
 """


def printRed(text):
    # Color red
    print "\033[31m{text}\033[0m".format(text=text)


def printGreen(text):
    # Color green
    print "\033[32m{text}\033[0m".format(text=text)


def printYellow(text):
    # Color yellow
    print "\033[33m{text}\033[0m".format(text=text)


def printBlue(text):
    # Color blue
    print "\033[34m{text}\033[0m".format(text=text)


def printPurple(text):
    # Color purple
    print "\033[35m{text}\033[0m".format(text=text)


def printCyan(text):
    # Color cyan
    print "\033[36m{text}\033[0m".format(text=text)


if __name__ == '__main__':
    import os

    if os.name == 'posix':
        printBlue("Blue text")
        printCyan("Cyan text")
        printGreen("Green text")
        printPurple("Purple text")
        printRed("Red text")
        printYellow("Yellow text")
