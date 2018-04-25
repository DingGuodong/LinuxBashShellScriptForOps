#!/usr/bin/env bash
# Created by PyCharm.
# File Name:              LinuxBashShellScriptForOps:rsync-directory-with-crontab.sh
# Version:                0.0.1
# Author:                 Guodong
# Author Email:           dgdenterprise@gmail.com
# URL:                    https://github.com/DingGuodong/LinuxBashShellScriptForOps
# Download URL:           https://github.com/DingGuodong/LinuxBashShellScriptForOps/tarball/master
# Create Date:            2018/4/25
# Create Time:            10:26
# Description:            
# Long Description:       
# Usage:                  
# References:             
# Prerequisites:          []
# Development Status:     3 - Alpha, 5 - Production/Stable
# Environment:            Console
# Intended Audience:      System Administrators, Developers, End Users/Desktop
# License:                Freeware, Freely Distributable
# Natural Language:       English, Chinese (Simplified)
# Operating System:       POSIX :: Linux
# Programming Language:   GNU bash :: 4+
# Topic:                  Utilities

# crontab setting
# */30 * * * * /bin/bash /root/rsync-directory-with-crontab.sh
# 30 19 * * * /bin/bash /root/rsync-directory-with-crontab.sh

# rsync task config
################
HOST="192.168.88.151"
SRC="/data"
DEST="/data/backup/from_$HOSTNAME"
USER="root"
SSH_OPTION="-p 22 -oStrictHostKeyChecking=no"
RSYNC_LOG_FILE="/tmp/rsync.log"
################

#SHELL=/bin/bash
#PATH=/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin

if test ${UID} -ne 0; then
    echo "ROOT ACCESS IS REQUIRED"
    echo "Only root can do that, but current user is '$USER', please use 'sudo $0' or run as root"
    exit 1
fi

ssh ${SSH_OPTION} ${USER}@${HOST} "mkdir -p ${DEST}"

/usr/bin/rsync -azurR \
    -e "ssh ${SSH_OPTION}" \
    --delete --delete-excluded \
    --log-file=${RSYNC_LOG_FILE} \
    ${SRC} ${USER}@${HOST}:${DEST}
