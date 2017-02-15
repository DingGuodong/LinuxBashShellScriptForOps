#!/usr/bin/python
# encoding: utf-8
# -*- coding: utf8 -*-
"""
Created by PyCharm.
File:               LinuxBashShellScriptForOps:checkDataIntegrity.py
User:               Guodong
Create Date:        2017/2/14
Create Time:        14:45

Python script to check data integrity on UNIX/Linux or Windows
accept options using 'docopt' module, using 'docopt' to accept parameters and command switch

Usage:
  checkDataIntegrity.py [-g FILE HASH_FILE]
  checkDataIntegrity.py [-c FILE HASH_FILE]
  checkDataIntegrity.py [-r HASH_FILE]
  checkDataIntegrity.py generate FILE HASH_FILE
  checkDataIntegrity.py validate FILE HASH_FILE
  checkDataIntegrity.py reset HASH_FILE
  checkDataIntegrity.py (--version | -v)
  checkDataIntegrity.py --help | -h | -?

Arguments:
  FILE                  the path to single file or directory to data protect
  HASH_FILE             the path to hash data saved

Options:
  -? -h --help          show this help message and exit
  -v --version          show version and exit

Example, try:
  checkDataIntegrity.py generate /tmp /tmp/data.json
  checkDataIntegrity.py validate /tmp /tmp/data.json
  checkDataIntegrity.py reset /tmp/data.json
  checkDataIntegrity.py -g /tmp /tmp/data.json
  checkDataIntegrity.py -c /tmp /tmp/data.json
  checkDataIntegrity.py -r /tmp/data.json
  checkDataIntegrity.py --help
"""
from docopt import docopt
import os
import sys
import hashlib


def get_hash_sum(filename, method="sha256", block_size=65536):
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
    elif "sha384" in method:
        checksum = hashlib.sha384()
    elif "sha512" in method:
        checksum = hashlib.sha512()
    else:
        raise RuntimeError("unsupported method %s" % method)

    with open(filename, 'rb') as f:
        buf = f.read(block_size)
        while len(buf) > 0:
            checksum.update(buf)
            buf = f.read(block_size)
        if checksum is not None:
            return checksum.hexdigest()
        else:
            return checksum


def makeDataIntegrity(path):
    path = unicode(path, 'utf8')  # For Chinese Non-ASCII character

    if not os.path.exists(path):
        raise RuntimeError("Error: cannot access %s: No such file or directory" % path)
    elif os.path.isfile(path):
        dict_all = dict()
        dict_all[os.path.abspath(path)] = get_hash_sum(path)
        return dict_all
    elif os.path.isdir(path):
        dict_nondirs = dict()
        dict_dirs = dict()
        for top, dirs, nondirs in os.walk(path, followlinks=True):
            for item in nondirs:
                # Do NOT use os.path.abspath(item) here, else it will make a serious bug because of
                # os.path.abspath(item) return "os.getcwd()" + "filename" in some case.
                dict_nondirs[os.path.join(top, item)] = get_hash_sum(os.path.join(top, item))
            for item in dirs:
                dict_dirs[os.path.join(top, item)] = r""
        dict_all = dict(dict_dirs, **dict_nondirs)
        return dict_all


def saveDataIntegrity(data, filename):
    import json
    data_to_save = json.dumps(data, encoding='utf-8')
    if not os.path.exists(os.path.dirname(filename)):
        os.makedirs(os.path.dirname(filename))
    with open(filename, 'wb') as f:
        f.write(data_to_save)


def readDataIntegrity(filename):
    import json
    if not os.path.exists(filename):
        raise RuntimeError("cannot open '%s' (No such file or directory)" % filename)
    with open(filename, 'rb') as f:
        data = json.loads(f.read())
    if data:
        return data


def remakeDataIntegrity(filename):
    def confirm(question, default=True):
        """
        Ask user a yes/no question and return their response as True or False.

        :parameter question:
        ``question`` should be a simple, grammatically complete question such as
        "Do you wish to continue?", and will have a string similar to " [Y/n] "
        appended automatically. This function will *not* append a question mark for
        you.
        The prompt string, if given,is printed without a trailing newline before reading.

        :parameter default:
        By default, when the user presses Enter without typing anything, "yes" is
        assumed. This can be changed by specifying ``default=False``.

        :return True or False
        """
        # Set up suffix
        if default:
            # suffix = "Y/n, default=True"
            suffix = "Y/n"
        else:
            # suffix = "y/N, default=False"
            suffix = "y/N"
        # Loop till we get something we like
        while True:
            response = raw_input("%s [%s] " % (question, suffix)).lower()
            # Default
            if not response:
                return default
            # Yes
            if response in ['y', 'yes']:
                return True
            # No
            if response in ['n', 'no']:
                return False
            # Didn't get empty, yes or no, so complain and loop
            print("I didn't understand you. Please specify '(y)es' or '(n)o'.")

    if os.path.exists(filename):
        if confirm("[warning] remake data integrity file \'%s\'?" % filename):
            os.remove(filename)
            print "[successful] data integrity file \'%s\' has been remade." % filename
            sys.exit(0)
        else:
            print "[warning] data integrity file \'%s\'is not remade." % filename
            sys.exit(0)
    else:
        print >> sys.stderr, "[error] data integrity file \'%s\'is not exist." % filename


def checkDataIntegrity(path_to_check, file_to_save):
    from time import sleep

    if not os.path.exists(file_to_save):
        print "[info] data integrity file \'%s\' is not exist." % file_to_save
        print "[info] make a data integrity file to \'%s\'" % file_to_save
        data = makeDataIntegrity(path_to_check)
        saveDataIntegrity(data, file_to_save)
        print "[successful] make a data integrity file to \'%s\', finished!" % file_to_save,
        print "Now you can use this script later to check data integrity."
    else:
        old_data = readDataIntegrity(file_to_save)
        new_data = makeDataIntegrity(path_to_check)
        error_flag = True
        for item in old_data.keys():
            if not old_data[item] == new_data[item]:
                print>> sys.stderr, new_data[item], item
                sleep(0.01)
                print "\told hash data is %s" % old_data[item], item
                error_flag = False
        if error_flag:
            print "[ successful ] passed, All files integrity is ok!"


if __name__ == '__main__':
    arguments = docopt(__doc__, version='1.0.0rc2')
    if arguments['-r'] or arguments['reset']:
        if arguments['HASH_FILE']:
            remakeDataIntegrity(arguments['HASH_FILE'])
    elif arguments['-g'] or arguments['generate']:
        if arguments['FILE'] and arguments['HASH_FILE']:
            checkDataIntegrity(arguments['FILE'], arguments['HASH_FILE'])
    elif arguments['-c'] or arguments['validate']:
        if arguments['FILE'] and arguments['HASH_FILE']:
            checkDataIntegrity(arguments['FILE'], arguments['HASH_FILE'])
    else:
        print >> sys.stderr, "bad parameters"
        sys.stderr.flush()
        print docopt(__doc__, argv="--help")
