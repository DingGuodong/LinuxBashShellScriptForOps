#!/usr/bin/python
# encoding: utf-8
# -*- coding: utf8 -*-
"""
Created by PyCharm.
File Name:              LinuxBashShellScriptForOps:pySettingSSHTrust.py
Version:                0.0.1
Author:                 Guodong
Author Email:           dgdenterprise@gmail.com
URL:                    https://github.com/DingGuodong/LinuxBashShellScriptForOps
Download URL:           https://github.com/DingGuodong/LinuxBashShellScriptForOps/tarball/master
Create Date:            2017/9/27
Create Time:            12:00
Description:            Setting up SSH Trust Between Two Servers or Self Trust (local)
Long Description:
References:
                        https://pypi.python.org/pypi/ssh-import-id/5.6
                        https://pypi.python.org/pypi/sshdeploy/1.1.4
                        https://github.com/kenkundert/sshdeploy
                        https://pypi.python.org/pypi?%3Aaction=browse
                        https://pypi.python.org/pypi/shlib/0.6.0
                        https://pypi.python.org/pypi/inform/1.9.0
                        https://pypi.python.org/pypi/abraxas/1.7

Prerequisites:          []
Development Status:     3 - Alpha, 5 - Production/Stable
Environment:            Console
Intended Audience:      System Administrators, Developers, End Users/Desktop
License:                Freeware, Freely Distributable
Natural Language:       English
Operating System:       POSIX :: Linux
Programming Language:   Python :: 2.6
Programming Language:   Python :: 2.7
Topic:                  Utilities
 """
import logging
import logging.handlers
import os
import re
import sys
import time


def initLoggerWithRotate(logPath="/var/log", logName=None, singleLogFile=True):
    current_time = time.strftime("%Y%m%d%H")
    if logName is not None and not singleLogFile:
        logPath = os.path.join(logPath, logName)
        logFilename = logName + "_" + current_time + ".log"
    elif logName is not None and singleLogFile:
        logPath = os.path.join(logPath, logName)
        logFilename = logName + ".log"
    else:
        logName = "default"
        logFilename = logName + ".log"

    if not os.path.exists(logPath):
        os.makedirs(logPath)
        logFilename = os.path.join(logPath, logFilename)
    else:
        logFilename = os.path.join(logPath, logFilename)

    logger = logging.getLogger(logName)
    log_formatter = logging.Formatter("%(asctime)s %(filename)s:%(lineno)d %(name)s %(levelname)s: %(message)s",
                                      "%Y-%m-%d %H:%M:%S")
    file_handler = logging.handlers.RotatingFileHandler(logFilename, maxBytes=104857600, backupCount=5)
    file_handler.setFormatter(log_formatter)
    stream_handler = logging.StreamHandler(sys.stderr)
    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)
    logger.setLevel(logging.DEBUG)
    return logger


def get_system_encoding():
    """
    The encoding of the default system locale but falls back to the given
    fallback encoding if the encoding is unsupported by python or could
    not be determined.  See tickets #10335 and #5846
    """
    import codecs
    import locale
    import sys
    mswindows = (sys.platform == "win32")
    try:
        encoding = locale.getdefaultlocale()[1] or ('ascii' if not mswindows else 'gbk')
        codecs.lookup(encoding)
    except Exception as e:
        del e
        encoding = 'ascii' if not mswindows else 'gbk'  # 'gbk' is Windows default encoding in Chinese language 'zh-CN'
    return encoding


DEFAULT_LOCALE_ENCODING = get_system_encoding()


def decoding(text):
    import sys

    mswindows = (sys.platform == "win32")

    msg = text
    if mswindows:
        try:
            msg = text.decode(DEFAULT_LOCALE_ENCODING)
            return msg
        except (UnicodeDecodeError, UnicodeEncodeError):
            pass
    return msg


def run(command, capture_stdout=False, suppress_stdout=False):
    import subprocess

    p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE,
                         stderr=subprocess.STDOUT)
    (stdout, stderr) = p.communicate()

    if p.returncode != 0:
        print "encountered an error (return code %s) while executing '%s'" % (p.returncode, command)
        if stdout is not None:
            print "Standard output:", decoding(stdout)
        if stderr is not None:
            print "Standard error:", decoding(stderr)
        if not capture_stdout:
            return False
        else:
            return ""
    else:

        if stdout is not None:
            if capture_stdout:
                return stdout
            else:
                if not suppress_stdout:
                    print decoding(stdout)
                return True


class TrustSSH:
    def __init__(self):
        self.user = os.getenv('USER') or 'root'
        self.home = os.getenv('HOME') or os.path.expanduser('~')
        self.ssh_dir = os.path.join(self.home, ".ssh")
        self.identity_file = os.path.join(self.ssh_dir, "id_rsa")
        self.authorized_keys_file = os.path.join(self.ssh_dir, "authorized_keys")
        self.host_rsa_key_private = "/etc/ssh/ssh_host_rsa_key"
        self.host_rsa_key_public = "/etc/ssh/ssh_host_rsa_key.pub"

        self.log = initLoggerWithRotate(logPath="", logName="SSHTrust", singleLogFile=True)
        self.log.setLevel(logging.INFO)

        self.generate_key()

        self.self_trust()

        self.hosts_registered = set()

    def usage(self):
        # displays a detailed description of the program and how to use it.
        pass

    def generate_key(self):
        # The generate command regenerates the SSH key pairs.
        if not os.path.exists(self.ssh_dir):
            os.makedirs(self.ssh_dir)
        if not os.path.exists(self.identity_file):
            run('ssh-keygen -N "" -f %s' % self.identity_file)

    def self_trust(self):
        if (not os.path.exists(self.authorized_keys_file)) and os.path.exists(self.host_rsa_key_private) \
                and os.path.exists(self.host_rsa_key_public):
            with open(self.host_rsa_key_public, 'r') as c:
                host_key_rsa = c.read()
            with open(self.authorized_keys_file, 'w') as f:
                f.write(host_key_rsa + '\n')
        else:
            with open(self.host_rsa_key_public, 'r') as c:
                host_key_rsa = c.read()
            with open(self.authorized_keys_file, 'r') as original:
                content = original.read()
            if host_key_rsa[0:16] not in content:
                with open(self.authorized_keys_file, 'a') as modified:
                    modified.write(host_key_rsa)

    def distribute_key(self, host):
        # The distribute command copies the SSH key pair to to the clients and the authorized_keys files to the servers.
        if host != '':
            run('ssh-copy-id -i {host_key} {user}@{host}'.format(host_key=self.host_rsa_key_private, user=self.user,
                                                                 host=host))
        pass

    def test_ssh_connect(self, host='localhost'):
        # The test command checks the connection with each of the hosts (the clients and servers).
        run('ssh -i /etc/ssh/ssh_host_rsa_key -p 22 -oStrictHostKeyChecking=no {user}@{host} "uname -a"'.format(
            user=self.user, host=host))
        pass

    def list_hosts(self):
        # Lists out the hosts include the servers and the clients that will receive the SSH key pairs.
        self.get_registered_hosts()
        for host in self.hosts_registered:
            print host.strip()

    def is_key_registered(self, key):
        fingerprint = self.get_fingerprint(key)
        self.update_registered_hosts()
        if fingerprint in self.hosts_registered:
            return True
        else:
            return False

    def update_registered_hosts(self):
        self.get_registered_hosts()

    def get_registered_hosts(self):
        if os.path.exists(self.authorized_keys_file):
            with open(self.authorized_keys_file, 'r') as original:
                content = original.read().strip()
                if content != '':
                    keys_list = content.split('\n')
                    for key in keys_list:
                        if key != "":  # in case blank line in self.authorized_keys_file
                            self.hosts_registered.add(self.get_fingerprint(key))

    @staticmethod
    def get_fingerprint(key):
        if run('echo \"{file}\" | ssh-keygen -l -f -'.format(file=key.strip()), capture_stdout=False,
               suppress_stdout=True):
            return run('echo \"{file}\" | ssh-keygen -l -f -'.format(file=key.strip()), capture_stdout=True)
        else:
            raise RuntimeError("invalid key")

    def get_fingerprint_short(self, key):
        fingerprint = self.get_fingerprint(key)
        if fingerprint != '' and isinstance(fingerprint, (unicode, str)):
            shortened_fingerprint = re.split('[ :]', fingerprint)[2]
            if shortened_fingerprint != '':
                return shortened_fingerprint[0:8]
            else:
                return ""
        else:
            raise RuntimeError("invalid key")  # won't be reached

    def add_key(self, key="", key_file=""):
        if key != '' and not self.is_key_registered(key):
            print "add key \'{key}\'(the 1st 8 chars) to {file} ...".format(key=self.get_fingerprint_short(key),
                                                                            file=self.authorized_keys_file)
            with open(self.authorized_keys_file, 'a') as modified:
                modified.write(key.strip() + '\n')

        if os.path.exists(key_file):
            import linecache
            for line in linecache.getlines(key_file):
                self.add_key(key=line)

    def clean(self):
        # removes the related files from each of the hosts
        pass


if __name__ == '__main__':
    s = TrustSSH()
    key1 = '''ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQCawuOgQup3Qc1OILytyH+u3S9te85ctEKTvzPtRjHfnEEOjpRS6v6/PsuDHplHO1PAm8cKbEZmqR9tg4mWSweosBYW7blUUB4yWfBu6cHAnJOZ7ADNWHHJHAYi8QFZd4SLAAKbf9J12Xrkw2qZkdUyTBVbm+Y8Ay9bHqGX7KKLhjt0FIqQHRizcvncBFHXbCTJWsAduj2i7GQ5vJ507+MgFl2ZTKD2BGX5m0Jq9z3NTJD7fEb2J6RxC9PypYjayXyQBhgACxaBrPXRdYVXmy3f3zRQ4/OmJvkgoSodB7fYL8tcUZWSoXFa33vdPlVlBYx91uuA6onvOXDnryo3frN1'''
    key2 = '''ssh-rsa AAAAB3NzaC1yc2EAAAABJQAAAIEAumQ2srRwd9slaeYTdr/dGd0H4NzJ3uQdBQABTe/nhJsUFWVG3titj7JiOYjCb54dmpHoi4rAYIElwrolQttZSCDKTVjamnzXfbV8HvJapLLLJTdKraSXhiUkdS4D004uleMpaqhmgNxCLu7onesCCWQzsNw9Hgpx5Hicpko6Xh0='''
    s.add_key(key1)
    s.add_key(key2)
    s.list_hosts()
