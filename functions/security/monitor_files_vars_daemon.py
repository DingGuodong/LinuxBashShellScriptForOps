#!/usr/bin/python
# encoding: utf-8
# -*- coding: utf8 -*-
"""
Created by PyCharm.
File:               LinuxBashShellScriptForOps:monitor_files_vars_daemon.py.py
User:               Guodong
Create Date:        2016/12/30
Create Time:        0:10

Supported OS:
    Linux only
Objects:
    FILES
      /var/log/
      /var/log/syslog
      /root/.bash_history
    VARS
      PROMPT_COMMAND

 """

import os
import sys
import hashlib
import json
import time

INSIGHT_HOME = "/var/lib/insight"
INSIGHT_HASH_FILE = os.path.join(INSIGHT_HOME, "hash.json")
INSIGHT_LOG_FILE = os.path.join(INSIGHT_HOME, "alter_log.json")
INSIGHT_SENSITIVE_FILE_LIST = [
    '/etc/passwd',
    '/etc/rc.local',
    '/etc/sysctl.conf',
]

INSIGHT_SENSITIVE_VAR_LIST = [
    'PROMPT_COMMAND',
]


def get_hash_sum(filename, method="md5", block_size=65536):
    if not os.path.exists(filename):
        raise RuntimeError("cannot open '%s' (No such file or directory)" % filename)
    if not os.path.isfile(filename):
        raise RuntimeError("'%s' :not a regular file" % filename)

    if "md5" in method:
        checksum = hashlib.md5()
    elif "sha1" in method:
        checksum = hashlib.sha1()
    elif "sha256" in method:
        checksum = hashlib.sha256()
    else:
        raise RuntimeError("unsupported method %s" % method)

    # if os.path.exists(filename) and os.path.isfile(filename):
    with open(filename, 'rb') as f:
        buf = f.read(block_size)
        while len(buf) > 0:
            checksum.update(buf)
            buf = f.read(block_size)
        if checksum is not None:
            return checksum.hexdigest()
        else:
            return checksum


def alter(filename):
    with open(INSIGHT_LOG_FILE, 'r') as f:
        alter_log = json.loads(f.read())
    if filename not in list(alter_log.keys()):
        print(filename)
        alter_log[filename] = True
        with open(INSIGHT_LOG_FILE, 'w') as f:
            f.write(json.dumps(alter_log, indent=4))


def main():
    old_hash_dict = dict()

    for sensitive_file in INSIGHT_SENSITIVE_FILE_LIST:
        old_hash_dict[sensitive_file] = get_hash_sum(sensitive_file)

    if not os.path.exists(INSIGHT_HOME):
        os.makedirs(INSIGHT_HOME)

    if not os.path.exists(INSIGHT_LOG_FILE):
        with open(INSIGHT_LOG_FILE, 'w+') as f:
            f.write("{}")

    if not os.path.exists(INSIGHT_HASH_FILE):
        with open(INSIGHT_HASH_FILE, 'w+') as f:
            f.write(json.dumps(old_hash_dict, indent=4))
    else:
        keep_running = True
        while keep_running:
            with open(INSIGHT_HASH_FILE, 'r') as f:
                safe_hash_dict = json.loads(f.read())
            for sensitive_file in INSIGHT_SENSITIVE_FILE_LIST:
                if get_hash_sum(sensitive_file) == safe_hash_dict[sensitive_file]:
                    pass
                else:
                    alter(sensitive_file)
            time.sleep(2)


if __name__ == '__main__':
    try:
        main()
    except (KeyboardInterrupt, SystemExit):
        sys.exit(0)
