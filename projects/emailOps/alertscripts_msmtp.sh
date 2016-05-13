#! /bin/bash

# Zabbix Email Alter
DEBUG=1
if [[ $DEBUG -gt 0 ]];then
    exec 2>>/tmp/zabbix_msmtp.log
    set -x
fi
FROM='example@example.com'
MSMTP_ACCOUNT='zabbix'
# Parameters (as passed by Zabbix):
#  $1 : Recipient
#  $2 : Subject
#  $3 : Message
recipient=$1
subject=$2
message=$3
date=`date --rfc-2822`
sed 's/$/\r/' <<EOF | /usr/bin/msmtp --account $MSMTP_ACCOUNT $recipient
From: <$FROM>
To: <$recipient>
Subject: $subject
Date: $date
$message
EOF