#!/usr/bin/python
# encoding: utf-8
# -*- coding: utf8 -*-
"""
Created by PyCharm.
File:               LinuxBashShellScriptForOps:getDiskUsage.py
User:               Guodong
Create Date:        2016/11/1
Create Time:        11:01
 """
import psutil

WindowsPartitionFSTypeList = ['NTFS', 'FAT32']

PosixPartitionFSTypeList = ['ext4', 'xfs']

FSTypeList = WindowsPartitionFSTypeList + PosixPartitionFSTypeList

# 5% reserved-blocks-percentage(tune2fs, dump2fs, man tune2fs)
# Normally, the default percentage of reserved blocks is 5%.
# tune2fs  -l <device> | grep "Reserved block"
# tune2fs -m 0 <device>
# dumpe2fs <device> |grep -i "Reserved block count"

# NB: the percentage is -5% than what shown by df due to
# reserved blocks that we are currently not considering:
# https://github.com/giampaolo/psutil/issues/829#issuecomment-223750462

# Linux (not sure about other UNIXes) by default reserves 5% of total disk space for the root user so that
# if, say, the user home directory fills the disk,
# the root user and the system will still have 5% of space to write into /var/log,
# not crash in general and also to avoid disk fragmentation:
# http://unix.stackexchange.com/a/7964/168884
for partition in psutil.disk_partitions():
    if partition.fstype in FSTypeList:
        diskUsage = psutil.disk_usage(partition.mountpoint)
        if diskUsage.percent > 95:
            print "Partition %s disk usage is overloaded!" % partition
        else:
            print partition.device, partition.mountpoint, diskUsage
