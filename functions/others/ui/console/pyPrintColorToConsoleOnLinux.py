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
    coreutils: ls.c
    static struct bin_str color_indicator[] =
  {
    { LEN_STR_PAIR ("\033[") },		/* lc: Left of color sequence */
    { LEN_STR_PAIR ("m") },		/* rc: Right of color sequence */
    { 0, NULL },			/* ec: End color (replaces lc+no+rc) */
    { LEN_STR_PAIR ("0") },		/* rs: Reset to ordinary colors */
    { 0, NULL },			/* no: Normal */
    { 0, NULL },			/* fi: File: default */
    { LEN_STR_PAIR ("01;34") },		/* di: Directory: bright blue */
    { LEN_STR_PAIR ("01;36") },		/* ln: Symlink: bright cyan */
    { LEN_STR_PAIR ("33") },		/* pi: Pipe: yellow/brown */
    { LEN_STR_PAIR ("01;35") },		/* so: Socket: bright magenta */
    { LEN_STR_PAIR ("01;33") },		/* bd: Block device: bright yellow */
    { LEN_STR_PAIR ("01;33") },		/* cd: Char device: bright yellow */
    { 0, NULL },			/* mi: Missing file: undefined */
    { 0, NULL },			/* or: Orphaned symlink: undefined */
    { LEN_STR_PAIR ("01;32") },		/* ex: Executable: bright green */
    { LEN_STR_PAIR ("01;35") },		/* do: Door: bright magenta */
    { LEN_STR_PAIR ("37;41") },		/* su: setuid: white on red */
    { LEN_STR_PAIR ("30;43") },		/* sg: setgid: black on yellow */
    { LEN_STR_PAIR ("37;44") },		/* st: sticky: black on blue */
    { LEN_STR_PAIR ("34;42") },		/* ow: other-writable: blue on green */
    { LEN_STR_PAIR ("30;42") },		/* tw: ow w/ sticky: black on green */
    { LEN_STR_PAIR ("30;41") },		/* ca: black on red */
    { 0, NULL },			/* mh: disabled by default */
    { LEN_STR_PAIR ("\033[K") },	/* cl: clear to end of line */
  };
 """


def printRed(text):
    # Color red
    print("\033[31m{text}\033[0m".format(text=text))


def printBrightRed(text):
    # Color bright red
    print("\033[01;31m{text}\033[0m".format(text=text))


def printGreen(text):
    # Color green
    print("\033[32m{text}\033[0m".format(text=text))


def printBrightGreen(text):
    # Color bright green
    print("\033[01;32m{text}\033[0m".format(text=text))


def printYellow(text):
    # Color yellow
    print("\033[33m{text}\033[0m".format(text=text))


def printBrightYellow(text):
    # Color bright yellow
    print("\033[01;33m{text}\033[0m".format(text=text))


def printBlue(text):
    # Color blue
    print("\033[34m{text}\033[0m".format(text=text))


def printBrightBlue(text):
    # Color bright blue
    print("\033[01;34m{text}\033[0m".format(text=text))


def printPurple(text):
    # Color purple, magenta
    print("\033[35m{text}\033[0m".format(text=text))


def printBrightPurple(text):
    # Color bright purple, magenta
    print("\033[01;35m{text}\033[0m".format(text=text))


def printCyan(text):
    # Color cyan
    print("\033[36m{text}\033[0m".format(text=text))


def printBrightCyan(text):
    # Color bright cyan
    print("\033[01;36m{text}\033[0m".format(text=text))


if __name__ == '__main__':
    import os

    if os.name == 'posix':
        printBlue("Blue text")
        printCyan("Cyan text")
        printGreen("Green text")
        printPurple("Purple text")
        printRed("Red text")
        printYellow("Yellow text")

        printBrightBlue("Bright Blue text")
        printBrightCyan("Bright Cyan text")
        printBrightGreen("Bright Green text")
        printBrightPurple("Bright Purple text")
        printBrightRed("Bright Red text")
        printBrightYellow("Bright Yellow text")
