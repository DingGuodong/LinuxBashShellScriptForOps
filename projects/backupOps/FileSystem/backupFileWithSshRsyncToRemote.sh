#!/usr/bin/env bash
# Function description:
# Backup filesystem using rsync

# Usage:
# bash backup.sh

# Birth Time:
# 2016-07-15 16:13:43.895515929 +0800

# Author:
# Open Source Software written by 'Guodong Ding <dgdenterprise@gmail.com>'
# Blog: http://dgd2010.blog.51cto.com/
# Github: https://github.com/DingGuodong

# Others:
# crontabs -- configuration and scripts for running periodical jobs
# SHELL=/bin/bash
# PATH=/sbin:/bin:/usr/sbin:/usr/bin
# MAILTO=root
# HOME=/
# For details see man 4 crontabs
# Example of job definition:
# .---------------- minute (0 - 59)
# |  .------------- hour (0 - 23)
# |  |  .---------- day of month (1 - 31)
# |  |  |  .------- month (1 - 12) OR jan,feb,mar,apr ...
# |  |  |  |  .---- day of week (0 - 6) (Sunday=0 or 7) OR sun,mon,tue,wed,thu,fri,sat
# |  |  |  |  |
# *  *  *  *  * user-name command to be executed
# m h  dom mon dow   command
# execute on 11:59 per sunday
# 59 11 * * */0 bash /path/to/backup.sh >/tmp/log_backup_fs_crontab_$(date +"\%Y\%m\%d\%H\%M\%S").log
# or
# execute on 23:59 per day
# 59 23 * * * bash /path/to/backup.sh >/tmp/log_backup_fs_crontab_$(date +"\%Y\%m\%d\%H\%M\%S").log

USER="`id -un`"
LOGNAME="$USER"
if [ $UID -ne 0 ]; then
    echo "WARNING: Running as a non-root user, \"$LOGNAME\". Functionality may be unavailable. Only root can use some commands or options"
fi

old_PATH=$PATH
declare -x PATH="/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games"

# Snapshot backup script
# Refer: https://github.com/gregrs-uk/snapshot-backup/

# directories to backup, separated by spaces
datadir_to_backup="/data/docker"
# backup location on remote server
# This path should not contain spaces, even if they are escaped
remote_destination="/data/backup/filesystem/10.6.28.135"
# ssh login to remote server
backup_server="root@10.6.28.28"
# set ssh options for backup server
ssh_option="-i /etc/ssh/ssh_host_rsa_key -p 22 -oStrictHostKeyChecking=no"
# log dir on local machine
#log_directory="/tmp/backup-filesystem-10.6.28.135"
log_directory="/tmp/"
# exclude file on local machine
exclude=""


# ------ END OF CONFIGURATION VARIABLES ------

# the following two variables should not need modification
datetime=`date +%Y%m%d%H%M%S`
date=`date +%Y%m%d`

# set log_directory for local backup logs
test -d ${log_directory} || mkdir -p ${log_directory}

# check directories exist and are accessible
ssh ${ssh_option} ${backup_server} "test -e $remote_destination || mkdir -p $remote_destination"

# make directory for this snapshot
ssh ${ssh_option} ${backup_server} "mkdir $remote_destination/$datetime-incomplete" || { echo "Could not create snapshot directory"; exit 1; }

# Refer:
#rsync -u -r -v -e ssh --progress --delete --chmod=D775 /path/to/documents/* your_server_name@your_domain:~/public_html/documents/ --exclude=.htaccess --exclude=.htaccess~
#rsync -azurR -e "ssh -i /etc/ssh/ssh_host_rsa_key -p 22 -oStrictHostKeyChecking=no" --log-file=/tmp/rsync.log --delete --delete-excluded testdir 10.6.28.28:/data/backup/filesystem/10.6.28.135


# do the rsync
# -a, --archive               archive mode; equals -rlptgoD (no -H,-A,-X)
# -r, --recursive             recurse into directories
# -R, --relative              use relative path names
# -u, --update                skip files that are newer on the receiver
# -z, --compress              compress file data during the transfer
rsync -azurR \
    -e "ssh $ssh_option" \
    --log-file=${log_directory}/backup_filesystem_rsync_${datetime}.log \
    --delete --delete-excluded \
    ${datadir_to_backup} \
    ${backup_server}:${remote_destination}/${datetime}-incomplete/

# change name of directory once rsync is complete
ssh ${ssh_option} ${backup_server} "mv $remote_destination/$datetime-incomplete $remote_destination/$datetime" || { echo "Could not rename directory after rsync"; exit 1; }

# link current to this backup
ssh ${ssh_option} ${backup_server} "test ! -d $remote_destination/current || rm -f $remote_destination/current" || { echo "Could not remove current backup link"; exit 1; }
ssh ${ssh_option} ${backup_server} "ln -s $remote_destination/$datetime $remote_destination/current" || { echo "Could not create current backup link"; exit 1; }

# remove backups older than 10 days
ssh ${ssh_option} ${backup_server} "find $remote_destination/* -maxdepth 0 -type d -mtime +10 -exec rm -rf {} \;" || { echo "Could not remove old backups"; exit 1; }

# remove local log files older than 10 days
find ${log_directory}/* -maxdepth 0 -type f -name *.log -mtime +10 -exec rm -rf '{}' \; || { echo "Could not remove old log files"; exit 1; }

declare -x PATH=${old_PATH}
