#! /bin/bash

# Zabbix Email alter shell script
# msmtp is an SMTP client
DEBUG=1
if [[ ${DEBUG} -gt 0 ]];then
    exec 2>>/tmp/zabbix_msmtp.log
    set -x
fi
FROM='example@example.com'
account_name='zabbix'
# Parameters (as passed by Zabbix):
#  $1 : Recipient
#  $2 : Subject
#  $3 : Message
recipient=$1
subject=$2
message=$3
date=`date --rfc-2822`
sed 's/$/\r/' <<eof | /usr/bin/msmtp --account ${account_name} ${recipient}
From: <${FROM}>
To: <${recipient}>
Subject: ${subject}
Date: ${date}
${message}
eof