#!/usr/bin/python
# encoding: utf-8
# -*- coding: utf8 -*-
"""
Created by PyCharm.
File:               LinuxBashShellScriptForOps:backupSmallFileToTarToLocal.py
User:               Guodong
Create Date:        2016/10/25
Create Time:        10:08

About this:
    “当你手上有一把锤子的时候，看所有的东西都是钉子；当你手上有个钉子的时候，看所有的东西都是锤子”
    解决问题要用恰当的工具。不要妄自追求大而全的工具去解决所有的问题。

    “如果没有了锤子，你还有石头！”

    if you do not have 'python', you have 'bash shell' at least.

 """
import os
# import zipfile
# import gzip
import tarfile
import time

# user defined variables
backup_source = r'..'
backup_target = r'C:\Users\Guodong\Desktop\target'  # please using abs path here.
backup_saveCounts = 10  # low priority
backup_saveDays = 10  # high priority


# end user defined variables


def usage():
    print '''backup files or directories to somewhere using python.
usage:
    python backupFileToLocal.py
or
    chmod +x backupFileToLocal.py && ./backupFileToLocal.py
    '''


if os.path.exists(backup_source):
    _backup_source = os.path.abspath(backup_source)
else:
    print "backup_source define error."
    usage()
    time.sleep(0.01)
    raise RuntimeError

if backup_target != '':
    # print os.path.basename(backup_target)
    if not os.path.exists(backup_target):
        os.makedirs(backup_target)
    else:
        # clean old backups if exist
        filesListToRemove = os.listdir(backup_target)[:-backup_saveCounts + 1]
        if len(filesListToRemove) != 0:
            print "Old backups found! Cleaning old backups..."
            for filename in filesListToRemove:
                fileToRemove = os.path.join(backup_target, filename)
                if time.time() - os.stat(fileToRemove).st_ctime > backup_saveDays * 24 * 3600:
                    os.remove(os.path.join(backup_target, filename))
    timeString = time.strftime('%Y%m%d-%H%M%S', time.localtime())
    filename = "backup_" + timeString + ".tar.gz"
    _backup_target = os.path.join(backup_target, filename)
else:
    print "backup_target define error."
    usage()
    time.sleep(0.01)
    raise RuntimeError

tar = tarfile.TarFile.gzopen(name=_backup_target, mode='w')

for top, dirs, nondirs in os.walk(_backup_source, followlinks=True):
    print 'dirs in backup source are: %s' % dirs
    print 'files in backup source are: %s' % nondirs
    for directory in dirs:
        abs_dir = os.path.join(top, directory)
        tar.add(abs_dir, arcname=directory)
        print "Directory added: %s" % abs_dir
    for filename in nondirs:
        abs_file = os.path.join(top, filename)
        tar.add(abs_file, arcname=filename)
        print "File added: %s" % abs_file

    # just need first layer, NOT recursive
    break
tar.close()
