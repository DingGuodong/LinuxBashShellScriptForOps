#!/usr/bin/env bash
# Created by PyCharm.
# File Name:              LinuxBashShellScriptForOps:watch-dog-for-service.sh
# Version:                0.0.1
# Author:                 dgden
# Author Email:           dgdenterprise@gmail.com
# URL:                    https://github.com/DingGuodong/LinuxBashShellScriptForOps
# Download URL:           https://github.com/DingGuodong/LinuxBashShellScriptForOps/tarball/master
# Create Date:            2019/7/24
# Create Time:            12:01
# Description:            a watch dog for a service written in bash shell script
# Long Description:       check service running status, bring it up when service fail upto n times
# Usage:                  */1 * * * * /root/watch-dog-for-service.sh
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

WDFS_DB_FILE="/tmp/.watch-dog-for-service.db"  # WDFS is stand for watch-dog-for-service.
WDFS_LOG_FILE="/tmp/watch-dog-for-service.log"
MAX_TRY_TIMES=1 # 1 means restart service after 2 times failure

ENABLE_DEBUG=1



function check_service_status(){
    status="0"
    ps aux | grep [a]pp_name || status="$?"  # RETURN="${?}", retval=$?
    if [[ "$status" = 0 ]]; then
        return 0
    else
        return ${status}
    fi

}

function get_db_value(){
    value_in_db=`cat ${WDFS_DB_FILE}`
    echo ${value_in_db}  # `echo` is more better than `cat` because of it is more easy to understand
}

function db_value_increase_one(){
    value_in_db=`get_db_value`
    echo "$(expr ${value_in_db} + 1)" > ${WDFS_DB_FILE}
}

function set_db_value_to_zero(){
    echo 0 > ${WDFS_DB_FILE}
}

function bring_up_service(){
    sudo -u ebt -i bash -c "cd /opt/corp_name/apps/app_name && /usr/bin/nohup /opt/tools/node-v6.9.5-linux-x64/bin/npm run start --app.name app_name >> /opt/corp_name/logs/app_name/app.log 2>&1 &"

}

function watch_dog(){
    status="0"
    check_service_status || status="$?"
    if [[ "$status" = 0 ]]; then
        set_db_value_to_zero
        [[ "$ENABLE_DEBUG" == 1 ]] && echo "$(date +%Y%m%d%H%M%S,%s) ok: process is running" | tee -a ${WDFS_LOG_FILE}
        return 0
    else
        value_in_db=`get_db_value`
        if [[ "$value_in_db" == "$MAX_TRY_TIMES" ]]; then
            [[ "$ENABLE_DEBUG" == 1 ]] && echo "$(date +%Y%m%d%H%M%S,%s) err: process is not found upto max times, try to start it" | tee -a ${WDFS_LOG_FILE}
            bring_up_service
            return 0
        else
            db_value_increase_one
        fi

        value_in_db=`get_db_value`
        [[ "$ENABLE_DEBUG" == 1 ]] && echo "$(date +%Y%m%d%H%M%S,%s) warn: process is not found, current times is $value_in_db" | tee -a ${WDFS_LOG_FILE}

    fi

}


function main(){
    watch_dog
}


main
