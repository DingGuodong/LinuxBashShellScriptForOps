#!/usr/bin/env bash
# Function description:
# Backup MySQL databases for each, backup schema and schema with data in one action.

# Usage:
# bash backup-mysql-using-mysqldump.sh

# Birth Time:
# 2020-06-29 18:02:43.895515929 +0800

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
# 59 11 * * */0 /path/to/BackupMysqlByDate.sh >/tmp/log_backup_mysql_$(date +"\%Y\%m\%d\%H\%M\%S").log
# or
# execute on 23:59 per day
# 59 23 * * * /path/to/BackupMysqlByDate.sh >/tmp/log_backup_mysql_$(date +"\%Y\%m\%d\%H\%M\%S").log

USER="$(id -un)"
LOGNAME="$USER"
if [[ ${UID} -ne 0 ]]; then
  echo "WARNING: Running as a non-root user, \"$LOGNAME\". Functionality may be unavailable. Only root can use some commands or options"
fi

old_PATH=$PATH
declare -x PATH="/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games"

using_socket=true # change this on demand

mysql_host=127.0.0.1
mysql_port=3306
mysql_username=root
mysql_password=dev
mysql_socket_file=/var/run/mysqld/mysqld.sock
mysql_backup_remote=false
mysql_basedir=/var/lib/mysql
save_old_backups_for_days=5
mysql_bin_mysql=/usr/bin/mysql
mysql_bin_mysqldump=/usr/bin/mysqldump
mysql_backup_dir=/backup/db/mysql

date_format_type_dir=$(date +%Y-%m-%d)
date_format_type_file=$(date +%Y%m%d%H%M%S)

# TODO(DingGuodong) we can send backups to oss(object store service)

# do this ONLY once
lock_file=$mysql_basedir/.backup_lock_file # do NOT set to $DEST, make sure $DEST (backup disk) exist
if [[ ! -f $lock_file ]]; then
  mkdir -p $mysql_backup_dir
  touch $lock_file
fi

test ! -d $mysql_backup_dir && echo "backup dir not exist, disk is down? exit now." && exit 1

echo "------------------------------------------------------------------------"
echo "=> do backup scheduler start at $(date +%Y%m%d%H%M%S)"

# TODO, check user privileges
# check user if have 'RELOAD,EVENT' privileges,etc
# backup role
# GRANT ALTER,ALTER ROUTINE,CREATE,CREATE ROUTINE,CREATE TEMPORARY TABLES,CREATE VIEW,DELETE,DROP,EXECUTE,INDEX,INSERT,LOCK TABLES,SELECT,UPDATE,SHOW VIEW,RELOAD,EVENT ON *.* TO 'dev'@"%";
# FLUSH PRIVILEGES;

[[ -d ${mysql_basedir} ]] && mysql_datadir=${mysql_basedir}/data || mysql_datadir="/var/lib/mysql"
[[ -x ${mysql_bin_mysql} ]] || mysql_bin_mysql="mysql"
[[ -x ${mysql_bin_mysqldump} ]] || mysql_bin_mysqldump="mysqldump"

if [[ ! -d ${mysql_datadir} ]]; then
  mysql_datadir="/var/lib/mysql" # in case basedir is right, but datadir is wrong
  if [[ ! -d ${mysql_datadir} ]]; then
    echo "WARNING: mysql datadir is not standard(this maybe a mistake) or mysql server is not installed on local filesystem."
  fi
fi

if [[ ! -x ${mysql_bin_mysql} ]]; then
  echo "mysql: command not found "
  exit 1
fi

if [[ ! -x ${mysql_bin_mysqldump} ]]; then
  echo "mysqldump: command not found "
  exit 1
fi

if [ $using_socket == "true" ]; then
  if [ ! -S $mysql_socket_file ]; then
    echo "ERROR 2002 (HY000): Can't connect to local MySQL server through socket '$mysql_socket_file' (2)"
    exit 1
  fi
  mysqldump_option_auth="-u${mysql_username} -S${mysql_socket_file}"
else
  # --host=${mysql_host} --port=${mysql_port} --user=${mysql_username} --password=${mysql_password}
  mysqldump_option_auth="-h${mysql_host} -P${mysql_port} -u${mysql_username} -p${mysql_password}"
fi

[[ -d ${mysql_backup_dir}/${date_format_type_dir} ]] || mkdir -p "${mysql_backup_dir}/${date_format_type_dir}"

mysql_databases_list=""
if [[ -d ${mysql_datadir} ]] || [[ "x${mysql_backup_remote}" != "xtrue" ]]; then
  # mysql_databases_list=$(find /var/lib/mysql -maxdepth 1 -type d -exec basename {} \; | sort | uniq)
  mysql_databases_list=$(find /var/lib/mysql -mindepth 1 -maxdepth 1 -type d -exec basename {} \;)
else
  # shellcheck disable=SC2086
  mysql_databases_list=$(${mysql_bin_mysql} $mysqldump_option_auth \
    --show-warnings=FALSE -e "show databases;" 2>/dev/null | grep -Eiv '(^database$|information_schema|performance_schema|^mysql$)')
fi

if [[ "x${mysql_databases_list}" == "x" ]]; then
  echo "no database is found to backup, aborted! "
  exit 1
fi

saved_IFS=$IFS
IFS=' '$'\t'$'\n'
for mysql_database in ${mysql_databases_list}; do
  # shellcheck disable=SC2086
  ${mysql_bin_mysqldump} $mysqldump_option_auth \
    --routines --events --triggers --single-transaction --flush-logs \
    --ignore-table=mysql.event --databases "${mysql_database}" 2>/dev/null |
    gzip >"${mysql_backup_dir}/${date_format_type_dir}/${mysql_database}-backup-${date_format_type_file}.sql.gz"

  # shellcheck disable=SC2181
  [[ $? -eq 0 ]] && echo "${mysql_database} backup successfully! " ||
    echo "${mysql_database} backup failed! "
  /bin/sleep 1

  # shellcheck disable=SC2086
  ${mysql_bin_mysqldump} $mysqldump_option_auth \
    --routines --events --triggers --single-transaction --flush-logs \
    --ignore-table=mysql.event --databases "${mysql_database}" --no-data 2>/dev/null |
    gzip >"${mysql_backup_dir}/${date_format_type_dir}/${mysql_database}-backup-${date_format_type_file}_schema.sql.gz"

  # shellcheck disable=SC2181
  [[ $? -eq 0 ]] && echo "${mysql_database} schema backup successfully! " ||
    echo "${mysql_database} schema backup failed! "
  /bin/sleep 1
done
IFS=${saved_IFS}

save_days=${save_old_backups_for_days:-10}
need_clean=$(find ${mysql_backup_dir} -maxdepth 1 -ctime +${save_days} -exec ls '{}' \;)
# if [[ ! -z ${need_clean} ]]; then
if [[ "x${need_clean}" != "x" ]]; then
  find ${mysql_backup_dir} -maxdepth 1 -ctime +${save_days} -exec rm -rf '{}' \;
  echo "old backups have been cleaned! "
else
  echo "nothing can be cleaned, skipped! "
fi

echo "=> do backup scheduler finished at $(date +%Y%m%d%H%M%S)"
echo -e "\n\n\n"

declare -x PATH=${old_PATH}
