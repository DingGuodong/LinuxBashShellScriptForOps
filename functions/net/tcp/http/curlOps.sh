#!/usr/bin/env bash
# Created by PyCharm.
# File:                 LinuxBashShellScriptForOps:${NAME}.sh
# User:                 Guodong
# Create Date:          2017/7/6
# Create Time:          16:33
# Function:             
# Note:                 curl --head --silent --show-error --connect-timeout 5 --retry 3 --retry-delay 2 --retry-max-time 5 --url http://www.baidu.com/ --output /dev/null
# Prerequisite:         
# Description:          Linux curl examples, sleep random seconds
# Reference:

url_list="
www.baidu.com
www.aliyun.com
www.163.com
"
for url in ${url_list}; do
    curl -sL -w "%{http_code} %{size_download}\\n" "${url}" -o /dev/null
done


# or
# Note: The file must use UNIX and OS X(LF, \n) line ending(Know as 'Line separators') not Windows(CRLF, \r\n),
# you can use 'dos2unix -n url.txt url_unix.txt' to change it easily,
# use 'dos2unix url.txt' will convert in old file mode
while IFS= read -r url
do
    curl -sL -w "%{http_code} %{size_download}\\n" "${url}" -o /dev/null
    sleep $((RANDOM % 7 + 3 ))
done < <(grep -v '^ *#' < url.txt)
