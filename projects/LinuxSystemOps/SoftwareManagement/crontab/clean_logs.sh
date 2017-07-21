#!/usr/bin/env bash
# Created by PyCharm.
# File:                 LinuxBashShellScriptForOps:${NAME}.sh
# User:                 Guodong
# Create Date:          2017/7/21
# Create Time:          9:11
# Function:             
# Note:                 
# Prerequisite:         
# Description:          clean logs in /tmp directory,
#                       replace big log file(log files to clean) with small log file($log_file)
# Reference:            
log_format="clean_log.log"
log_path="$HOME"
log_file="$log_path/$log_format"
save_days=10

log_path_clean="/tmp"
find ${log_path_clean} -type f -name "*.log" -maxdepth 1 -ctime ${save_days} -execdir rm -f '{}' \;
rc=$?  # return code always is 0 so far
if [ ${rc} -eq 0 ]; then
    logger -s "log clean successfully!"
    cat >>${log_file}<<eof
    "date": $(date +%Y%m%d%H%M%S),
    "operation": "find ${log_path_clean} -type f -name "*.log" -maxdepth 1 -ctime ${save_days} -execdir rm -f '{}' \;",
    "msg": "clean ok",

eof
else
    echo "log clean failed!"
    exit 1
fi

if test -s ${log_file}; then
    find ${log_path} -type f -name "*.log" -maxdepth 1 -ctime ${save_days} -execdir rm -f '{}' \;
fi
