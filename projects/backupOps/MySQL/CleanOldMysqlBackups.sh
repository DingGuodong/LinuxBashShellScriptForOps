#!/usr/bin/env bash
mysql_backup_dir=/data/backup/db/mysql
save_old_backups_for_days=5
save_days=${save_old_backups_for_days:-10}
need_clean=$(find ${mysql_backup_dir} -maxdepth 1 -mtime +${save_days} -exec ls '{}' \;)
if [ "x${need_clean}" != "x" ]; then
    find ${mysql_backup_dir} -maxdepth 1 -mtime +${save_days} -exec rm -rf '{}' \;
    echo "old backups have been cleaned! "
else
    echo "nothing can be cleaned, skipped! "
fi
