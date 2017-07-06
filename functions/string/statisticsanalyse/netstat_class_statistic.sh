#!/usr/bin/env bash
# Created by PyCharm.
# File:                 LinuxBashShellScriptForOps:${NAME}.sh
# User:                 Guodong
# Create Date:          2017/7/6
# Create Time:          9:13
# Function:             
# Note:                 
# Prerequisite:         
# Description:          
# Reference:

# 查询本地IP已经使用的端口
netstat -ltn | sed '1,2d' | awk -F'[ :]+' '{print $5}'
LC_ALL=C netstat -ltn | sed '1,2d' | awk '{print $4}' | awk -F ':' '{print $NF}' | sort -n

# 按端口号排序查询监听的端口
netstat -nltp | awk 'NR>2{split($4,a,":");t=sprintf("%5d",a[2]);b[t]=$0}END{for(i=0;i++<asorti(b,c);)print b[c[i]]}'
netstat -nolpt | awk 'BEGIN{print "PID/SER\tIP\tPORT"}/^t/{print gensub("([^,]+),(.*):(.*)","\\1 \\2 \\3","g",$7","$4)}' |column -t | sort -k3n

# 查询外部IP打开本地端口的统计情况
netstat -anot | awk '{print $5}' | awk -F ':' '{print $1}' | grep -v 192.168 | sort | uniq -c| sort -n -r | head -n 5
netstat -anopt | grep 6379 | awk -F[\ ]+ '{print $5}' | awk -F':' '{print $1}' | sort | uniq -c |sort -n -r

# 查看系统的网络连接数情况确认是否有较大的链接数
netstat -n | awk '/^tcp/ {++S[$NF]} END {for(a in S) print a, S[a]}'