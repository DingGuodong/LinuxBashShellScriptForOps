#!/bin/bash
# learn from https://docs.openstack.org/ops-guide/ops-backup-recovery.html#database-backups
backup_dir="/var/lib/backups/mysql"
filename="${backup_dir}/mysql-`hostname`-`eval date +%Y%m%d`.sql.gz"
# Dump the entire MySQL database
/usr/bin/mysqldump --opt --all-databases | gzip > ${filename}
# Delete backups older than 7 days
find ${backup_dir} -ctime +7 -type f -delete
