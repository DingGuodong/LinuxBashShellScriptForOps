#!/usr/bin/env bash

# Function description:
# set logrotate for logfile

# Usage:
# bash setLogrotate.sh </absolutely/path/to/logfile/name1> [/absolutely/path/to/logfile/name2...]

# Birth Time:
# 2016-05-30 10:07:13.289403529 +0800

# Author:
# Open Source Software written by 'Guodong Ding <dgdenterprise@gmail.com>'
# Blog: http://dgd2010.blog.51cto.com/
# Github: https://github.com/DingGuodong

# Test result:
# test passed on CentOS 6.7 and Ubuntu 14.04.4 LTS


# Refer:
#    /etc/cron.daily/logrotate
#    /etc/logrotate.conf
#    /etc/logrotate.conf
#    /etc/logrotate.d
#    /etc/logrotate.d/rsyslog

set -e
# Usage: $0 </absolutely/path/to/logfile/name1> [/absolutely/path/to/logfile/name2...]
if [ $# -eq 0 ]; then
    echo "Usage: bash $0 </absolutely/path/to/logfile/name1> [/absolutely/path/to/logfile/name2...]"
    exit 1
fi

# TODO(Guodong Ding) check if there are repeated configs for same logfile

for logfile in "$@"; do
    if test -f ${logfile}; then
        echo "set logrotate for $logfile ... "
        logrotate_config_file="/etc/logrotate.d/customized_logfile_${RANDOM}_$$"
        cat >>${logrotate_config_file} <<eof
${logfile} {
    daily
#    su user group
    rotate 12
    size 10M
    missingok
    notifempty
    compress
}

eof
        logrotate --debug ${logrotate_config_file} >/dev/null 2>&1 # -d, --debug    Don't do anything, just test (implies -v)
        if test "$?" = "0"; then
            echo "set logrotate for $logfile successfully! "
        else
            echo "set logrotate for $logfile failed: bad config file or logrotate command is not exist or system incompatible , please alter to system administrators. "
        fi

    else
        echo "set logrotate for $logfile failed: Bad logfile, `ls $logfile`"
    fi

done
set +e