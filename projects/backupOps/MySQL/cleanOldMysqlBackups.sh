#!/usr/bin/env bash
mysql_backup_dir=/data/backup/db/mysql
save_old_backups_for_days=5
save_days=${save_old_backups_for_days:-10}
# use -ctime to replace -mtime, replace -mtime with -ctime option
need_clean=$(find ${mysql_backup_dir} -maxdepth 1 -ctime +${save_days} -exec ls '{}' \;)
if [ "x${need_clean}" != "x" ]; then
    find ${mysql_backup_dir} -maxdepth 1 -ctime +${save_days} -exec rm -rf '{}' \;
    echo "old backups have been cleaned! "
else
    echo "nothing can be cleaned, skipped! "
fi
