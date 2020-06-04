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
# Long Description:       see `man rsync`: rsync - a fast, versatile, remote (and local) file-copying tool
#                         Rsync is a fast and extraordinarily versatile file copying tool.
#                         It can copy locally, to/from another host over any remote shell, or to/from a remote rsync daemon.
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

# shellcheck disable=SC2029
ssh "${SSH_OPTION}" ${USER}@${HOST} "mkdir -p ${DEST}"

# -a --> archive mode; equals -rlptgoD (no -H,-A,-X)
# -c --> skip based on checksum, not mod-time & size
# -q --> suppress non-error messages
# -u --> skip files that are newer on the receiver
# -v --> increase verbosity
# -z --> compress file data during the transfer
/usr/bin/rsync -az \
  -e "ssh ${SSH_OPTION}" \
  --delete --delete-excluded \
  --log-file=${RSYNC_LOG_FILE} \
  ${SRC} ${USER}@${HOST}:"${DEST}"
