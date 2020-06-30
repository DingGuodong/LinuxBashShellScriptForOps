# Cli
```shell script
mysql_host=""
mysql_port=""
mysql_username=""
mysql_password=""
mysql_database=""
mysql_export_out_filename=export_${mysql_database}_$(date +%Y%m%d%H%M%S).sql
mysqldump --host=${mysql_host} --port=${mysql_port} --user=${mysql_username} --password=${mysql_password}\
    --routines --events --triggers --single-transaction\
    --ignore-table=mysql.event --databases ${mysql_database} > ${mysql_export_out_filename}

mysqldump --host=${mysql_host} --port=${mysql_port} --user=${mysql_username} --password=${mysql_password}\
    --routines --events --triggers --single-transaction --flush-logs\
    --ignore-table=mysql.event --databases ${mysql_database} > ${mysql_export_out_filename}
```

>. use '-F' or '--flush-logs' with _mysqldump_ is recommended, it will be useful 
when restore database data with full-backup and binlog

## xtrabackup cli refs

xtrabackup can be used ONLY on the Server which running MySQL Server Instance. If MySQL Server run in docker, 
xtrabackup will throw a error such as 'xtrabackup: Can't change dir to '/var/lib/mysql/' (Errcode: 2 - No such file or directory)'

[Download Percona XtraBackup 8.0](https://www.percona.com/downloads/Percona-XtraBackup-LATEST/)
[Download Percona XtraBackup 2.4](https://www.percona.com/downloads/Percona-XtraBackup-2.4/LATEST/)

> xtrabackup based on MySQL server 5.7.13 can NOT connect to MySQL Server 8.x
> such as 'xtrabackup version 2.4.9 based on MySQL server 5.7.13 Linux (x86_64) (revision id: a467167cdd4)' 
> error msg: Failed to connect to MySQL server: Authentication plugin 'caching_sha2_password' cannot be loaded: 
>/usr/lib/plugin/caching_sha2_password.so: cannot open shared object file: No such file or directory.

[Authentication plugin 'caching_sha2_password' cannot be loaded](https://stackoverflow.com/questions/49194719/authentication-plugin-caching-sha2-password-cannot-be-loaded)
```sql
select @@version;
use mysql;
select plugin,host,user from mysql.user;
ALTER USER 'root'@'%' IDENTIFIED WITH mysql_native_password BY 'mysqlpassword';
```

```shell script
sudo apt install -y percona-xtrabackup
sudo mkdir -p /backup/db/mysql/xtrabackup_backupfiles
sudo xtrabackup --host=127.0.0.1 --port=3306 --user=root --password=mysqlpassword --backup --target-dir=/backup/db/mysql/xtrabackup_backupfiles
sudo xtrabackup --defaults-file=/etc/my.cnf --user=root -socket=/var/run/mysqld/mysqld.sock --backup --target-dir=/backup/db/mysql/xtrabackup_backupfiles
```
