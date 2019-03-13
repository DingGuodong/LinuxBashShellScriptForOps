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
Updates:            Improve code to optimize experience
 """

# Although using Python to backup mysql database is not a pythonic way because of
# using the system command mysqldump and xtrabackup is inevitable,
# but we need backup on Windows sometimes.

import os
import sys
import time
from subprocess import call

mysql_host = '127.0.0.1'
mysql_port = 3306
mysql_user = 'root'
mysql_password = 'Y0dPCxyLPFpbw'
mysql_db_list = ['cmdb', 'kissops', 'devdb', 'itoms_schema']  # dbs to backup

backups_save_path = os.path.join(os.path.expanduser('~'), 'Desktop')

enable_interactive_mode = False
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
        print("default setting is accepted!")
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

    try:
        with open(os.devnull, 'w') as null:
            call("%s --help" % mysqldump_bin_file, stdout=null)  # run command without output
    except WindowsError as e:
        if e.args[0] == 2:
            print "%s: command not found" % mysqldump_bin_file
        else:
            print "some wrong with %s" % mysqldump_bin_file
        sys.exit(e.args[0])

    if os.path.exists(backups_save_path):
        backup_base_dir = backups_save_path
    else:
        print("The backups will be stored into %s" % backups_save_path)
        if confirm("The directory where the backup is stored does not exist, are you wish to create it?"):
            os.makedirs(backups_save_path)
            backup_base_dir = backups_save_path
        else:
            HOME = os.path.expanduser('~')  # both Windows and Linux is works
            backup_base_dir = os.path.join(HOME, 'Desktop')
            print("The backups will be stored into %s" % backup_base_dir)
            if not confirm("Accept it?"):
                print("Aborted!")
                sys.exit(2)
    for db in mysql_db_list:
        backup_file = os.path.join(backup_base_dir, '{db}_{time}.sql'.format(db=db, time=time.strftime("%Y%m%d%H%M%S")))
        if print_cli:
            print "{mysqldump} {options} {database} > {path} 2>nul".format(mysqldump=mysqldump_bin_file,
                                                                           options=mysqldump_parameters,
                                                                           database=db, path=backup_file)
        print "mysqldump database %s ..." % db
        # Suppress error messages in Windows commandline
        return_code = call("{mysqldump} {options} {database} > {path} 2> nul".format(mysqldump=mysqldump_bin_file,
                                                                                     options=mysqldump_parameters,
                                                                                     database=db, path=backup_file),
                           shell=True)
        if return_code != 0:
            print('%s database backup finished with exit code %d' % (db, return_code))
        else:
            print('%s database backup successfully!' % db)


if __name__ == '__main__':
    if enable_interactive_mode:
        mysql_auth()
    backup()
