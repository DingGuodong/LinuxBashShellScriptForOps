#!/usr/bin/python
# encoding: utf-8
# -*- coding: utf8 -*-
"""
Created by PyCharm.
File:               LinuxBashShellScriptForOps:backupMySQLOnWindows.py
User:               Guodong
Create Date:        2017/7/4
Create Time:        16:32
Description:        backup mysql server data using mysqldump on Windows server

 """

import os
from subprocess import call

mysql_host = '127.0.0.1'
mysql_port = 0
mysql_user = 'root'
mysql_password = ''
mysql_db_list = ['mysql', 'devdb', 'itoms_schema']  # dbs to backup

enable_interactive_mode = False  # same concept as 'bash -i'
print_cli = False  # if print mysqldump cli, so that admin user can refer it


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
        suffix = "Y/n"
    else:
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


def mysql_auth():
    global mysql_host, mysql_port, mysql_user, mysql_password
    print '''default mysql client setting is:
        host: {host}
        port: {port}
        user: {user}
        password: {password}
    '''.format(host=mysql_host, port=mysql_port, user=mysql_user, password=mysql_password)
    if confirm('Is this right?'):
        pass
    else:
        import getpass
        mysql_host = raw_input('Enter MySQL host:')
        mysql_port = raw_input('Enter MySQL port:')
        mysql_user = raw_input('Enter MySQL user:')
        mysql_password = getpass.getpass("Enter MySQL password: ")  # do run it in Pycharm or other pseudo-terminal etc

        print '''mysql client setting is:
                host: {host}
                port: {port}
                user: {user}
                password: {password}
            '''.format(host=mysql_host, port=mysql_port, user=mysql_user, password=mysql_password)


def backup():
    mysqldump_bin_file = 'mysqldump'
    mysqldump_parameters = '-u {user} --password=\"{password}\" -h {host} -P {port} --force \
--routines --events --triggers --single-transaction \
--databases'.format(user=mysql_user, password=mysql_password, host=mysql_host, port=mysql_port)

    HOME = os.path.expanduser('~')  # both Windows and Linux is works
    backup_base_dir = os.path.join(HOME, 'Desktop')

    for db in mysql_db_list:
        backup_file = os.path.join(backup_base_dir, '{db}.sql'.format(db=db))
        if print_cli:
            print "{mysqldump} {options} {database} > {path}".format(mysqldump=mysqldump_bin_file,
                                                                     options=mysqldump_parameters,
                                                                     database=db, path=backup_file)
        print "mysqldump database %s ..." % db
        # Suppress error messages in Windows commandline
        call("{mysqldump} {options} {database} > {path} 2> nul".format(mysqldump=mysqldump_bin_file,
                                                                       options=mysqldump_parameters,
                                                                       database=db, path=backup_file), shell=True)
        print 'finished'


if __name__ == '__main__':
    if enable_interactive_mode:
        mysql_auth()
    backup()
