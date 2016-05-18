#!/usr/bin/env bash
#
# Function description:
# Use this script to initialize system after full refresh installation
#
# Usage:
# bash centos6-init.sh
#
# Birth Time:
# 2016-05-17 10:19:33.005064327 +0800
#
# Author:
# Open Source Software written by 'Guodong Ding <dgdenterprise@gmail.com>'
# Blog: http://dgd2010.blog.51cto.com/
# Github: https://github.com/DingGuodong
#

# debug option
#_XTRACE_FUNCTIONS=$(set +o | grep xtrace)
#set -o xtrace

# define user friendly messages
header="
Use this script to initialize system after full refresh installation
"

# user defined variables
user_defined_=""
# end user defined variables

# pretreatment
# end pretreatment

# Public header
# =============================================================================================================================
# resolve links - $0 may be a symbolic link
# learn from apache-tomcat-6.x.xx/bin/catalina.sh
PRG="$0"

while [ -h "$PRG" ]; do
  ls=`ls -ld "$PRG"`
  link=`expr "$ls" : '.*-> \(.*\)$'`
  if expr "$link" : '/.*' > /dev/null; then
    PRG="$link"
  else
    PRG=`dirname "$PRG"`/"$link"
  fi
done

# Get standard environment variables
PRGDIR=`dirname "$PRG"`

# echo color function, smarter, learn from lnmp.org lnmp install.sh
function echo_r (){
    # Color red: Error, Failed
    [ $# -ne 1 ] && return 1
    echo -e "\033[31m$1\033[0m"
}
function echo_g (){
    # Color green: Success
    [ $# -ne 1 ] && return 1
    echo -e "\033[32m$1\033[0m"
}
function echo_y (){
    # Color yellow: Warning
    [ $# -ne 1 ] && return 1
    echo -e "\033[33m$1\033[0m"
}
function echo_b (){
    # Color blue: Debug Level 1
    [ $# -ne 1 ] && return 1
    echo -e "\033[34m$1\033[0m"
}

function echo_p (){
    # Color purple: Debug Level 2
    [ $# -ne 1 ] && return 1
    echo -e "\033[35m$1\033[0m"
}

function echo_c (){
    # Color cyan: friendly prompt, Level 1
    [ $# -ne 1 ] && return 1
    echo -e "\033[36m$1\033[0m"
}

# end echo color function, smarter

WORKDIR="$PRGDIR"
# end public header
# =============================================================================================================================

USER="`id -un`"
LOGNAME="$USER"
if [ $UID -ne 0 ]; then
    echo "WARNING: Running as a non-root user, \"$LOGNAME\". Functionality may be unavailable. Only root can use some commands or options"
fi

# Name: doDeploy.sh

# define user friendly messages
header="
Function: Execute this shell script to deploy Java projects built by Maven automatically.
License: Open source software
"

check_network_connectivity(){
    echo_b "checking network connectivity ... "
    network_address_to_check=8.8.4.4
    stable_network_address_to_check=114.114.114.114
    ping_count=2
    ping -c ${ping_count} ${network_address_to_check} >/dev/null
    retval=$?
    if [ ${retval} -ne 0 ] ; then
        if ping -c ${ping_count} ${stable_network_address_to_check} >/dev/null;then
            echo_g "Network to $stable_network_address_to_check succeed! "
            echo_y "Note: network to $network_address_to_check failed once! maybe just some packages loss."
        elif ! ip route | grep default >/dev/null; then
            echo_r "Network is unreachable, gateway is not set."
            exit 1
        elif ! ping -c2 $(ip route | awk '/default/ {print $3}') >/dev/null; then
            echo_r "Network is unreachable, gateway is unreachable."
            exit 1
        else
            echo_r "Network is blocked! "
            exit 1
        fi
    elif [ ${retval} -eq 0 ]; then
        echo_g "Check network connectivity passed! "
    fi
}

check_name_resolve(){
    echo_b "checking DNS name resolve ... "
    target_name_to_resolve="github.com"
    stable_target_name_to_resolve="www.aliyun.com"
    ping_count=1
    if ! ping  -c${ping_count} ${target_name_to_resolve} >/dev/null; then
        echo_y "Name lookup failed for $target_name_to_resolve with $ping_count times "
        if ping  -c${ping_count} ${stable_target_name_to_resolve} >/dev/null; then
            echo_g "Name lookup success for $stable_target_name_to_resolve with $ping_count times "
        fi
        [ -f /etc/resolv.conf ] && cp /etc/resolv.conf /etc/resolv.conf_$(date +%Y%m%d%H%M%S)~
        cat >/etc/resolv.conf<<eof
nameserver 114.114.114.114
nameserver 8.8.4.4
eof
    check_name_resolve
    else
        echo_g "Check DNS name resolve passed! "
        return
    fi

}

command_exists() {
    # which "$@" >/dev/null 2>&1
    command -v "$@" >/dev/null 2>&1
}

check_command_can_be_execute(){
    command_exists
}

function main(){
    lock_filename="lock_$$_$RANDOM"
    lock_filename_full_path="/var/lock/subsys/$lock_filename"
    if ( set -o noclobber; echo "$$" > "$lock_filename_full_path") 2> /dev/null;then
        trap 'rm -f "$lock_filename_full_path"; exit $?' INT TERM EXIT
        # do
        test -z ${header} || echo_b "$header"
        echo $@
        # done
        rm -f "$lock_filename_full_path"
        trap - INT TERM EXIT
    else
        echo "Failed to acquire lock: $lock_filename_full_path"
        echo "held by $(cat ${lock_filename_full_path})"
fi

}

main $@
