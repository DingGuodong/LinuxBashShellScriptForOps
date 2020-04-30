#!/usr/bin/env bash
# Created by PyCharm.
# File Name:              LinuxBashShellScriptForOps:check-command-outputs.sh
# Version:                0.0.1
# Author:                 Guodong
# Author Email:           dgdenterprise@gmail.com
# URL:                    https://github.com/DingGuodong/LinuxBashShellScriptForOps
# Download URL:           https://github.com/DingGuodong/LinuxBashShellScriptForOps/tarball/master
# Create Date:            2019/5/20
# Create Time:            9:54
# Description:            
# Long Description:       持续查询某个端口如22的网络连接情况，将时间戳和连接信息写入文件
#                         应用场景：
#                           1. 对外攻击，查被攻击对象；遭受攻击，查攻击对象
# Usage:                  
# References:             https://www.tldp.org/LDP/abs/html/string-manipulation.html
# Prerequisites:          []
# Development Status:     3 - Alpha, 5 - Production/Stable
# Environment:            Console
# Intended Audience:      System Administrators, Developers, End Users/Desktop
# License:                Freeware, Freely Distributable
# Natural Language:       English, Chinese (Simplified)
# Operating System:       POSIX :: Linux
# Programming Language:   GNU bash :: 4+
# Topic:                  Utilities

statistics_file="statistics-$(date +%Y%m%d%H%M%S).log"

touch "${statistics_file}"
echo "tail -f $statistics_file"

while true; do
    msg=$(netstat -anop|grep -E '(:3128|:8080)')
    if test -n "${msg::15}"; then  # bash string manipulation(Substring Extraction), like str[:15] in Python
        now=$(date +%Y%m%d%H%M%S)
        data=$(netstat -anop|grep -E '(:3128|:8080)')
        echo "$now $data">>"${statistics_file}"
    fi
done

