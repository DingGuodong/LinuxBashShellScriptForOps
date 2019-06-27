#!/usr/bin/env bash
# Created by PyCharm.
# File Name:              LinuxBashShellScriptForOps:backup-remote-files-to-local.sh
# Version:                0.0.1
# Author:                 dgden
# Author Email:           dgdenterprise@gmail.com
# URL:                    https://github.com/DingGuodong/LinuxBashShellScriptForOps
# Download URL:           https://github.com/DingGuodong/LinuxBashShellScriptForOps/tarball/master
# Create Date:            2019/6/26
# Create Time:            16:40
# Description:            rsync remote files to local
# Long Description:       
# Usage:                  30 21 * * * /root/backup-gitlab-repos.sh >>/tmp/backup-gitlab-repos.log
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

# remote host setting
backup_host="10.27.15.12"
backup_ssh_port=22
backup_ssh_user="root"
backup_ssh_private_key="$HOME/.ssh/id_rsa"
backup_data_dir="/data"
backup_data_dirname="gitlab_repos"
backup_log="/tmp/backupGitLabByClone.log"

# local host setting
local_data_dir="/data/backup/gitlab_repos"
RSYNC_LOG_FILE="/tmp/gitlab_repos_rsync.log"
save_days=5

function run() {
    SSH_OPTION="-oStrictHostKeyChecking=no"
    ssh ${SSH_OPTION} -p ${backup_ssh_port} ${backup_ssh_user}@${backup_host} bash -c \"$@\"
}

function is_backup_finished(){
    is_backup_finished=0
    max_try_times=6
    goon=1
    while test ${goon} -eq 1; do
        is_all_true=0
        for _ in `seq ${max_try_times}`; do
            md5sum_1=`run md5sum ${backup_log}`
            sleep 5
            md5sum_2=`run md5sum ${backup_log}`

            if test "${md5sum_1}" == "${md5sum_2}"; then
                is_all_true=$(($is_all_true + 1))
            else
                is_backup_finished=1
            fi
        done

        if test ${is_all_true} -eq ${max_try_times}; then
            goon=0
        else
            continue
        fi
    done

    return ${goon}
}

function do_archive_files(){
    run "cd ${backup_data_dir} && tar zcfP ${backup_data_dirname}.tgz ${backup_data_dirname}"
}

function do_rm_archive_files(){
    run "cd ${backup_data_dir} && rm -f ${backup_data_dirname}.tgz"
}

function do_clean_local_files(){
    find  ${local_data_dir} -mtime +${save_days} -exec rm -rf '{}' \;

}

echo "$(date +%s)  check backup finished or not ..."
is_backup_finished
res=$?
if test ${res} -eq 0 ; then
    echo "$(date +%s)  archive backup files ..."
    do_archive_files
else
    echo "ERR: transfer remote files to local failed, please transfer by manual after few minutes or change crontab job"
fi

echo "$(date +%s)  rsync remote files to local ..."
test ! -d ${local_data_dir}/$(date -I) && mkdir -p ${local_data_dir}/$(date -I)
rsync -azurR \
    -e "ssh ${SSH_OPTION}" \
    --delete --delete-excluded \
    --log-file=${RSYNC_LOG_FILE} \
    ${backup_ssh_user}@${backup_host}:${backup_data_dir}/${backup_data_dirname}.tgz ${local_data_dir}/$(date -I)
res=$?
if test ${res} -ne 0 ; then
    echo "ERR: rsync failed"
fi

echo "$(date +%s)  remove used archived files ..."
do_rm_archive_files

echo "$(date +%s)  clean old backups in local ..."
do_clean_local_files

echo "$(date +%s)  SUCCESS"
