#!/usr/bin/env bash
#
# Function description:
# Add some hosts record into /etc/hosts file
#
# Usage:
# bash check_who_login_and_record.sh
#
# Birth Time:
# 2016-04-27 9:45:00.956620365 +0800 #date +'%Y-%m-%d %H:%M:%S.%N %z'
#
# Author:
# Open Source Software written by 'Guodong Ding <dgdenterprise@gmail.com>'
# Blog: http://dgd2010.blog.51cto.com/
# Github: https://github.com/DingGuodong
#

# Print the commands being run so that we can see the command that triggers
# an error.  It is also useful for following along as the install occurs.
# same as set -u
# Save trace setting
_XTRACE_FUNCTIONS=$(set +o | grep xtrace)
set -o xtrace


# Function description: backup files
# Note: accept $@ parameters
backup_files(){
    set -o errexit
    if [ "$#" -eq 0 ]; then
        return 1
    fi
    file_list=$@
    operation_date_time="_`date +"%Y%m%d%H%M%S"`"
    log_filename=".log_$$_$RANDOM"
    log_filename_full_path=/tmp/${log_filename}
    touch ${log_filename_full_path}
    old_IFS=$IFS
    IFS=" "
    for file in ${file_list};do
        real_file=$(realpath ${file})
        [ -f ${real_file} ] && cp ${real_file} ${file}${operation_date_time}~
        [ -f ${log_filename_full_path} ] && echo "\mv -f $file$operation_date_time~ $file" >>${log_filename_full_path}
    done
    IFS="$old_IFS"
    set +o errexit
    return 0
}

# Function description:
rollback_files(){
    [ -f ${log_filename_full_path} ] && . ${log_filename_full_path}
    \rm -f ${log_filename_full_path}
    exit 2
}

function main(){
    lock_filename="lock_$$_$RANDOM"
    lock_filename_full_path="/var/lock/subsys/$lock_filename"
    if ( set -o noclobber; echo "$$" > "$lock_filename_full_path") 2> /dev/null;then
        trap 'rm -f "$lock_filename_full_path"; exit $?' INT TERM EXIT
        # do
        backup_files $@ || rollback_files
        # done
        rm -f "$lock_filename_full_path"
        trap - INT TERM EXIT
    else
        echo "Failed to acquire lock: $lock_filename_full_path"
        echo "held by $(cat ${lock_filename_full_path})"
fi

}

main $@


