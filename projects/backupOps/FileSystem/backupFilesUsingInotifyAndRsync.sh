#!/bin/bash
# Created by PyCharm.
# File Name:              LinuxBashShellScriptForOps:backupFilesUsingInotifyAndRsync.sh
# Version:                0.0.1
# Author:                 Guodong
# Author Email:           dgdenterprise@gmail.com
# URL:                    https://github.com/DingGuodong/LinuxBashShellScriptForOps
# Download URL:           https://github.com/DingGuodong/LinuxBashShellScriptForOps/tarball/master
# Create Date:            2018/4/9
# Create Time:            15:14
# Description:            backup files using inotify-tools and rsync
# Long Description:       If there are a lot of files to rsync, more CPU and memory is required, CPU is sensitive
#                         In this case, I think use "rsync + crontab" is better than "inotify + rsync"
#                         Before use this script, you should run rsync singly in console to check system load.
# Usage:                  nohup bash ./backupFilesUsingInotifyAndRsync.sh >/dev/null 2>&1 &
# References:
# Prerequisites:          []
# Development Status:     3 - Alpha, 5 - Production/Stable
# Environment:            Console
# Intended Audience:      System Administrators, Developers, End Users/Desktop
# License:                Freeware, Freely Distributable
# Natural Language:       English, Chinese (Simplified)
# Operating System:       POSIX :: Linux
# Topic:                  Utilities

# setting
################
HOST="192.168.88.151"
SRC="/data"
DEST="/data/backup/from_$HOSTNAME"
USER="root"
SSH_OPTION="-p 22 -oStrictHostKeyChecking=no"
RSYNC_LOG_FILE="/tmp/rsync.log"
################

ssh ${SSH_OPTION} ${USER}@${HOST} "mkdir -p ${DEST}"

# run once time via check if log file exist
test -f  ${RSYNC_LOG_FILE} || /usr/bin/rsync -azurR \
    -e "ssh ${SSH_OPTION}" \
    --delete --delete-excluded \
    --log-file=${RSYNC_LOG_FILE} \
    ${SRC} ${USER}@${HOST}:${DEST}

# fs.inotify.max_user_watches = 8192
sysctl -w fs.inotify.max_user_watches=999999
# echo 999999 > /proc/sys/fs/inotify/max_user_watches

/usr/bin/inotifywait \
    -mrq \
    --format '%w%f' \
    -e modify,delete,create,attrib \
    ${SRC} \
| while read file; do
    test -e ${file} && /usr/bin/rsync -azurR \
        -e "ssh ${SSH_OPTION}" \
        --delete --delete-excluded \
        --log-file=${RSYNC_LOG_FILE} \
        ${file} ${USER}@${HOST}:${DEST}
done
