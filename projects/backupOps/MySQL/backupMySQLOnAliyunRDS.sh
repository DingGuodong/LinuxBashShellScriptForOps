#!/usr/bin/env bash
# Created by PyCharm.
# File:                 LinuxBashShellScriptForOps:backupMySQLOnAliyunRDS.sh
# User:                 Guodong
# Create Date:          2017/7/3
# Create Time:          15:29
# Function:             backup Aliyun RDS MySQL using mysqldump
# Note:                 
# Prerequisite:         
# Description:
# Reference:            https://github.com/amalucelli/aws-rds-backup

# crontab -e
# 59 23 * * * /root/backupMySQLOnAliyunRDS.sh >/tmp/log_backup_mysql_$(date +"\%Y-\%m").log

function log() {
    local msg=${1?}
    echo -ne $(date +['%Y-%m-%d %H:%M:%S'])" $msg\n"
}

function removeOldBackup() {
    local instanceID=$(echo ${mysqlHost} | cut -f1-2 -d.)
    local backupDir="${backupBaseDir}/${backupType}/${backupDB}/${instanceID}"
    log "Removing local backup files older than ${backupRetentionDays} days"
    for f in $(find ${backupDir} -mindepth 1 -mtime +${backupRetentionDays}); do
       log "${f}"
    done;
    find ${backupDir} -mindepth 1 -mtime +${backupRetentionDays} -delete
}

function doBackup() {
    local instanceID=$(echo ${mysqlHost} | cut -f1-2 -d.)
    local localDate=$(date +%Y-%m-%d)
    local backupDir="${backupBaseDir}/${backupType}/${backupDB}/${instanceID}/${localDate}"
    if [[ ! -d ${backupDir} ]]; then
        log "Creating local backup folder \"${backupDir}\""
        mkdir -p ${backupDir}
    fi
    saved_IFS=$IFS
    IFS=' '$'\t'$'\n'
    for db in ${dbList}; do
        log "Dumping \"${db}\" into \"${backupDir}/${db}-$(date +%d-%m-%Y-%H-%M).sql.gz\""
        mysqldump -u ${mysqlUser} -p${mysqlPwd} -h ${mysqlHost} -P${mysqlPort} --force \
            --routines --events --triggers --single-transaction \
            --databases "${db}" 2>/dev/null | gzip -c > ${backupDir}/${db}-$(date +%d-%m-%Y-%H-%M).sql.gz
        mysqldump -u ${mysqlUser} -p${mysqlPwd} -h ${mysqlHost} -P${mysqlPort} --force \
            --routines --events --triggers --single-transaction \
            --no-data --databases "${db}" 2>/dev/null | gzip -c > ${backupDir}/${db}-$(date +%d-%m-%Y-%H-%M)_schema.sql.gz
    done;
    IFS=${saved_IFS}
    removeOldBackup
}

# backup settings
backupType="rds"
backupDB="mysql"
backupRetentionDays=5
backupBaseDir="/data/backup"

# mysql settings
mysqlHost="rm-xxx.mysql.rds.aliyuncs.com"
mysqlPort=3306
mysqlUser=""
mysqlPwd=''
dbList="db1 db2 db3"


doBackup
