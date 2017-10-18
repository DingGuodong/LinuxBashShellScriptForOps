#!/usr/bin/env bash
################################################################
# Created by PyCharm.
# File:                 LinuxBashShellScriptForOps:alterscript_sendmailbycurl.sh
# User:                 Guodong
# Create Date:          2017/6/30
# Create Time:          11:04
# Function:             send email by curl
# Note:                 
# Prerequisite:         curl >= 7.20 or latest version, Internet access both way
# Description:
################################################################


cat >mail.txt<<eof
From: "Chris.Ding <chris.ding@gmail.com>
To: "DingGuodong" <uberurey_ups@163.com>
Subject: This is a test mail from curl

Hi Guodong,
I'm sending this mail with curl from my gmail.com account.
Bye!
eof


## curl -V
#curl 7.54.1 (x86_64-pc-linux-gnu) libcurl/7.54.1 OpenSSL/1.0.1e zlib/1.2.3 libssh2/1.4.2
#Release-Date: 2017-06-14
#Protocols: dict file ftp ftps gopher http https imap imaps pop3 pop3s rtsp scp sftp smb smbs smtp smtps telnet tftp
#Features: Largefile NTLM NTLM_WB SSL libz UnixSockets HTTPS-proxy

#wget -c https://curl.haxx.se/download/curl-7.54.1.tar.gz
#tar zxf curl-7.54.1.tar.gz
#cd curl-7.54.1
#./configure --prefix=/usr/local/curl
#make install
#ls /usr/local/curl/
#mv /usr/lib64/libcurl.so.4 /usr/lib64/libcurl.so.4~
#ln -s /usr/local/curl/lib/libcurl.so.4 /usr/lib64/libcurl.so.4
#ldconfig
#cd

export PATH=/usr/local/curl/bin:$PATH
curl --url 'smtp://smtp.gmail.com:465' --ssl-reqd \
  --mail-from 'chris.ding@gmail.com' --mail-rcpt 'uberurey_ups@163.com' \
  --upload-file mail.txt --user 'chris.ding@gmail.com:password' --insecure
