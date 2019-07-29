#!/usr/bin/env bash
#!/bin/bash
# delete all spaces and comments of specialized file, using with $@ filename
[[ "$1" == "" ]] && echo "delete all spaces and comments of specialized file, using with $0 filename" && exit 1
if cat -A "$1" | grep '\^M\\$' >/dev/null || file "$1" | grep "with CRLF line terminators" >/dev/null ; then
    command -v dos2unix >/dev/null 2>&1 || yum -q -y install dos2unix || apt-get -qq -y install dos2unix
    dos2unix "$1" >/dev/null
fi
if test -f "$1" && file "$1" | grep "XML" >/dev/null; then
    command -v tidy >/dev/null 2>&1 || yum -q -y install tidy || apt-get -qq -y install tidy
    tidy -quiet -asxml -xml -indent -wrap 1024 --hide-comments 1 "$1"
elif test -f "$1"; then
    grep -v \# "$1" | grep -v ^\; |grep -v ^$ | grep -v "^\ *$"
fi
# Others:
# cat -A /path/to/filename
# sed -e '/^#/d;/^$/d' $1
# Refer: https://github.com/mysfitt/nocomment/blob/master/nocomment.sh
# grep -Ev '^\s*#|^//|^\s\*|^/\*|^\*/' $1 | grep -Ev '^$|^\s+$'