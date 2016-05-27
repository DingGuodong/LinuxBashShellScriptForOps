#!/usr/bin/env bash
#
# Function description:
#
# About Interactive and non-interactive shells and scripts
# Interactive script to be one that requires input from the user,
# usually with read statements or positional parameters
# Non-interactive shells run without human intervention.
# Many administrative and system maintenance scripts are likewise non-interactive.
#
# Usage:
# bash check_who_login_and_record.sh
#
# Birth Time:
# 2016-04-22 10:41:00.956620365 +0800 #date +'%Y-%m-%d %H:%M:%S.%N %z'
#
# Author:
# Open Source Software written by 'Guodong Ding <dgdenterprise@gmail.com>'
# Blog: http://dgd2010.blog.51cto.com/
# Github: https://github.com/DingGuodong
#

# Print the commands being run so that we can see the command that triggers
# an error.  It is also useful for following along as the install occurs.
# same as set -u
# Save trace setting
#_XTRACE_FUNCTIONS=$(set +o | grep xtrace)
#set -o xtrace

# Check if a command already exists
function command_exists() {
    # which "$@" >/dev/null 2>&1
    command -v "$@" >/dev/null 2>&1
}

parameters_restrict_more_then_one(){
    # More Info: http://www.gnu.org/software/bash/manual/bashref.html#Shell Parameter Expansion
    if [ "$#" -eq 0 ]; then
        return 1
    fi
}

# TODO validate command ipcalc if exists
check_ip_manipulation_tool_if_exist(){
    ID=
    DISTRIB_ID=
    if command_exists ipcalc; then
        return 0
    elif command_exists lsb_release; then
        DISTRO=$(lsb_release -is 2>/dev/null)
        test "$DISTRO" = "Ubuntu" -o "$DISTRO" = "Debian" && apt-get -qq -y install ipcalc
        local retval=$?
        if test "$retval" -eq 0; then
            command_exists ipcalc && echo "Install ipcalc successfully, "$(which ipcalc)" is found! "
            return 0
        else
            return ${retval}
        fi
    elif [ -f /etc/os-release ] && . /etc/os-release;then
        echo "Can NOT find ipcalc in $PATH, try install it on system which type is $ID ... "
        test "$ID" = "ubuntu" -o "$ID" = "debian" && apt-get -qq -y install ipcalc
        local retval=$?
        if test "$retval" -eq 0; then
            command_exists ipcalc && echo "Install ipcalc successfully, "$(which ipcalc)" is found! "
            return 0
        else
            return ${retval}
        fi
    elif [ -f /etc/lsb-release ] && . /etc/lsb-release;then
        echo "Can NOT find ipcalc in $PATH, try install it on system which type is $ID ... "
        test "$DISTRIB_ID" = "Ubuntu" -o "$DISTRIB_ID" = "Debian" && apt-get -qq -y install ipcalc
        local retval=$?
        if test "$retval" -eq 0; then
            command_exists ipcalc && echo "Install ipcalc successfully, "$(which ipcalc)" is found! "
            return 0
        else
            return ${retval}
        fi
    else
        echo "Fatal error: Can NOT find ipcalc in $PATH, and system type is $ID, failed! "
        exit 1
    fi

}
# /etc/sysconfig/network-scripts/network-functions-ipv6 (CentOS Linux release 7.2.1511 (Core))
## Test a given IPv6 address for validity
#  $1: <IPv6 address>
# return code: 0=ok 1=not valid
ipv6_test_ipv6_addr_valid() {
    ipcalc -cs6 $1
}

## Test a given IPv4 address for validity
#  $1: <IPv4 address>
# return code: 0=ok 1=not valid
ipv6_test_ipv4_addr_valid() {
    ipcalc -cs4 $1
}

## Test a given IPv4 address for not a private but unicast one
#  $1: <IPv4 address>
# return code: 0=ok 1=argument error 10=private or not unicast
ipv6_test_ipv4_addr_global_usable() {
    local fn="ipv6_test_ipv4_addr_global_usable"

    local testipv4addr_globalusable=$1


    if [ -z "$testipv4addr_globalusable" ]; then
                return 1
    fi

    # Test for a globally usable IPv4 address now
    # test 0.0.0.0/8
    /bin/ipcalc --network $testipv4addr_globalusable 255.0.0.0   | LC_ALL=C grep -q "NETWORK=0\.0\.0\.0"     && return 10
    # test 10.0.0.0/8     (RFC 1918 / private)
    /bin/ipcalc --network $testipv4addr_globalusable 255.0.0.0   | LC_ALL=C grep -q "NETWORK=10\.0\.0\.0"    && return 10
    # test 127.0.0.0/8    (loopback)
    /bin/ipcalc --network $testipv4addr_globalusable 255.0.0.0   | LC_ALL=C grep -q "NETWORK=127\.0\.0\.0"   && return 10
    # test 169.254.0.0/16 (APIPA / DHCP link local)
    /bin/ipcalc --network $testipv4addr_globalusable 255.255.0.0 | LC_ALL=C grep -q "NETWORK=169\.254\.0\.0" && return 10
    # test 172.16.0.0/12  (RFC 1918 / private)
    /bin/ipcalc --network $testipv4addr_globalusable 255.240.0.0 | LC_ALL=C grep -q "NETWORK=172\.16\.0\.0"  && return 10
    # test 192.168.0.0/16 (RFC 1918 / private)
    /bin/ipcalc --network $testipv4addr_globalusable 255.255.0.0 | LC_ALL=C grep -q "NETWORK=192\.168\.0\.0" && return 10
    # test 224.0.0.0/3    (multicast and reserved, broadcast)
    /bin/ipcalc --network $testipv4addr_globalusable 224.0.0.0   | LC_ALL=C grep -q "NETWORK=224\.0\.0\.0"   && return 10

    return 0
}

function is_reserved_ip_address(){
    # Refer to: https://en.wikipedia.org/wiki/Reserved_IP_addresses
    # /etc/sysconfig/network-scripts/network-functions-ipv6 (CentOS Linux release 7.2.1511 (Core))
    test_ipv4_addr_global_usable=$1
    ipcalc -cs4 "$test_ipv4_addr_global_usable"
    ipcalc -cs6 "$test_ipv4_addr_global_usable"
    /bin/ipcalc --network "$test_ipv4_addr_global_usable" 255.0.0.0   | LC_ALL=C grep -q "NETWORK=0\.0\.0\.0"     && return 10
    /bin/ipcalc --network "$test_ipv4_addr_global_usable" 255.0.0.0   | LC_ALL=C grep -q "NETWORK=10\.0\.0\.0"    && return 10
    /bin/ipcalc --network "$test_ipv4_addr_global_usable" 255.0.0.0   | LC_ALL=C grep -q "NETWORK=127\.0\.0\.0"   && return 10
    /bin/ipcalc --network "$test_ipv4_addr_global_usable" 255.255.0.0 | LC_ALL=C grep -q "NETWORK=169\.254\.0\.0" && return 10
    /bin/ipcalc --network "$test_ipv4_addr_global_usable" 255.240.0.0 | LC_ALL=C grep -q "NETWORK=172\.16\.0\.0"  && return 10
    /bin/ipcalc --network "$test_ipv4_addr_global_usable" 255.255.0.0 | LC_ALL=C grep -q "NETWORK=192\.168\.0\.0" && return 10
    /bin/ipcalc --network "$test_ipv4_addr_global_usable" 224.0.0.0   | LC_ALL=C grep -q "NETWORK=224\.0\.0\.0"   && return 10
}

function return_ip_addr_if_is_global_usable(){
    ipv6_test_ipv4_addr_global_usable $1
    local retval=$?
    if test "$retval" -eq 0; then
        return 0
    else
        return ${retval}
    fi
}

function get_current_login_users_ipaddress(){
    # return a single result or a list
    old_IFS=$IFS
    IFS=" "
    original_ip_list="`w -h | awk '/[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}/ {print $3}'`"
    ignore_reduplicate_ip_list="`echo "$original_ip_list" | tr ' ' '\n' | sort | uniq`"
    IFS="$old_IFS"
    if test ! -z "$ignore_reduplicate_ip_list"; then
        for ip in "$ignore_reduplicate_ip_list";do
            echo "$ip"
        done
    else
        return 1
    fi

}

function get_current_login_users_ipaddress_and_times(){
    # AI: who -q # show all login names and number of users logged on
    echo -e "\t- Total count of users is: $(w -h | wc -l)"
    command_exists w && w -h | awk '/[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}/ {a[$3]++}END{for (i in a) print "\t- Still logged in IP address : "i", count is: "a[i]}'
}

show_current_logged_in_users_ip_address(){
    echo "Current logged in users from ip address are: "
    get_current_login_users_ipaddress_and_times
    echo
    current_logged_in_users_ipaddress=$(get_current_login_users_ipaddress)
    echo "Current logged in users from ip address are:"
    for ip in ${current_logged_in_users_ipaddress}; do
        echo -e "\t- $ip"
    done
    echo
}

show_current_logged_in_users_ip_address_from_public_network(){
    some_user_logged_in_from_public_network=0
    for ip in ${current_logged_in_users_ipaddress}; do
        if return_ip_addr_if_is_global_usable "$ip"; then
            some_user_logged_in_from_public_network=1
            echo -n "Current logged in users ip address from public network are:"
            echo "$ip"
        fi
    done
    if test ${some_user_logged_in_from_public_network} -eq 0; then
        echo "NO logged in users ip address from public network."
    fi
    echo
}

show_extra_information_from_sys_call(){
    echo "Show who is logged on and what they are doing by \"w\" : "
    command_exists w && w
    echo
    echo "Show a list of last logged in users, top 10 users show by \"last\" : "
    command_exists last && last | head -n10
}

function main(){
    lock_filename="lock_$$_$RANDOM"
    lock_filename_full_path="/var/lock/subsys/$lock_filename"
    if ( set -o noclobber; echo "$$" > "$lock_filename_full_path") 2> /dev/null;then
        trap 'rm -f "$lock_filename_full_path"; exit $?' INT TERM EXIT
        # do
        check_ip_manipulation_tool_if_exist
        show_current_logged_in_users_ip_address
        show_current_logged_in_users_ip_address_from_public_network
        show_extra_information_from_sys_call
        # done
        rm -f "$lock_filename_full_path"
        trap - INT TERM EXIT
    else
        echo "Failed to acquire lock: $lock_filename_full_path"
        echo "held by $(cat ${lock_filename_full_path})"
fi

}

main