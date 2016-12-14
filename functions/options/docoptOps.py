#!/usr/bin/python
# encoding: utf-8
# -*- coding: utf8 -*-
"""
Created by PyCharm.
File:               LinuxBashShellScriptForOps:docoptOps.py
User:               Guodong
Create Date:        2016/12/12
Create Time:        17:33

Example of program with many options using docopt, control system service.
Usage:
  docoptOps.py SERVICE_NAME SERVICE_ACTION
  docoptOps.py SERVICE_ACTION SERVICE_NAME
  docoptOps.py --version | -v
  docoptOps.py --help | -h
Arguments:
  SERVICE_NAME  service name
  SERVICE_ACTION service action
Options:
  -h --help            show this help message and exit
  -v --version         show version and exit
"""
from docopt import docopt
import sys

service_action = ['start', 'stop', 'restart', 'reload', 'status']

if __name__ == '__main__':
    arguments = docopt(__doc__, version='1.0.0rc2')
    if arguments['SERVICE_ACTION'] in service_action:
        pass
    elif arguments['SERVICE_NAME'] in service_action:
        tmp = arguments['SERVICE_ACTION']
        arguments['SERVICE_ACTION'] = arguments['SERVICE_NAME']
        arguments['SERVICE_NAME'] = tmp
    else:
        print arguments
        sys.exit(1)
    print "service", arguments['SERVICE_NAME'], arguments['SERVICE_ACTION']
