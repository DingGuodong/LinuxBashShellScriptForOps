#! /bin/bash
# Zabbix Email alert shell script(**Deprecated**)
# msmtp is an SMTP client
# TODO(DingGuodong) set a configuration for msmtp
# refer: https://askubuntu.com/questions/1289573/msmtp-sendmail-account-default-not-found-no-configuration-file-available-sys

DEBUG=1
if [[ ${DEBUG} -gt 0 ]]; then
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
date=$(date --rfc-2822)
sed 's/$/\r/' <<eof | /usr/bin/msmtp --account ${account_name} "${recipient}"
From: <${FROM}>
To: <${recipient}>
Subject: ${subject}
Date: ${date}
${message}
eof
