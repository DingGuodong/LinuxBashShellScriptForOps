# Cli
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
