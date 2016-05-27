#!/usr/bin/env bash
#
# Function description:
# Use this script to initialize system after full refresh installation
# Do NOT modify anything expect for "user defined variables" unless you know what it means and what are you doing.

# Try most best to refer to more general and minimal principle, UNIX philosophy
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
user_defined_hostname=""
user_defined_username=""
user_defined_user_can_run_sudo=true # true or false
user_defined_log_absolute_path=""
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

#WORKDIR="`realpath ${WORKDIR}`"
WORKDIR="`readlink -f ${PRGDIR}`"

# end public header
# =============================================================================================================================

USER="`id -un`"
LOGNAME="$USER"
if [ $UID -ne 0 ]; then
    echo_y "WARNING: Running as a non-root user, \"$LOGNAME\". Functionality may be unavailable. Only root can use some commands or options."
    echo_y "Retry to using \"sudo bash $0 $@\"."
fi

command_exists() {
    # which "$@" >/dev/null 2>&1
    command -v "$@" >/dev/null 2>&1
}

check_command_can_be_execute(){
    [ $# -ne 1 ] && return 1
    command_exists $1
}

function check_user_defined_variables(){
    # TODO(Guodong Ding) continue
    test -z $user_defined_hostname
    test -z $user_defined_username
    test -z $user_defined_user_can_run_sudo
    test -z $user_defined_log_absolute_path

}

function backup_single_file(){
    set -o errexit
    if [ "$#" -ne 1 ]; then
        return 1
    fi
    backup_filename_origin="$1"
    operation_date_time="`date +"%Y%m%d%H%M%S"`"
    backup_filename_prefix=".backup_"
    backup_filename_suffix="_origin_$operation_date_time~"
    backup_filename_target="$backup_filename_prefix$backup_filename_origin$backup_filename_suffix"
    test -f $backup_filename_origin && cp $backup_filename_origin $backup_filename_target
    set +o errexit

}

# Function description: backup files without directory support
# Note: accept $@ parameters, such as '$0 file1 file2 file3'
# Usage: backup_files $@ || rollback_files
backup_files(){
    set -o errexit
    if [ "$#" -eq 0 ]; then
        return 1
    fi
    file_list=$@
    operation_date_time="_`date +"%Y%m%d%H%M%S"`"
    log_filename=".log_$0_$$_$RANDOM"
    if test -z $user_defined_log_absolute_path; then
        log_filename_full_path=/tmp/$log_filename
    else
        log_filename_full_path=$user_defined_log_absolute_path
    fi
    touch $log_filename_full_path
    old_IFS=$IFS
    IFS=" "
    for file in $file_list;do
        # is there a bin named 'realpath' ?
        real_file=$(readlink -f $file)
        [ -f $real_file ] && cp $real_file $file$operation_date_time~
        [ -f $log_filename_full_path ] && echo "\mv -f $file$operation_date_time~ $file" >>$log_filename_full_path
    done
    IFS="$old_IFS"
    set +o errexit
    return 0
}

# Function description: rollback files
rollback_files(){
    [ -f $log_filename_full_path ] && . $log_filename_full_path
    \rm -f $log_filename_full_path
    exit 2
}


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
        eval_md5sum_of_nameserver_config="`md5sum /etc/resolv.conf | awk '{ print $1 }'`"
        if test ${eval_md5sum_of_nameserver_config} = "674ea91675cdfac353bffbf49dc593c3"; then
            echo_y "Nameserver config file is validated, but name lookup failed for $target_name_to_resolve with $ping_count times"
            return 0
        fi
        [ -f /etc/resolv.conf ] && cp /etc/resolv.conf /etc/resolv.conf_$(date +%Y%m%d%H%M%S)~
        cat >/etc/resolv.conf<<eof
nameserver 114.114.114.114
nameserver 8.8.4.4
eof
    check_name_resolve
    else
        echo_g "Check DNS name resolve passed! "
        return 0
    fi
}

function set_hostname_fqdn_format(){
    current_hostname_fqdn="`hostname -A`"
    dot_appear_times_to_match_fqdn_rule=`echo "$current_hostname_fqdn" | grep -o '\.' | wc -l`
    if test $dot_appear_times_to_match_fqdn_rule -gt 1; then
        echo_g "current hostname $current_hostname_fqdn is a fqdn name, check passed! "
    else
        if test ! -z $user_defined_hostname; then
            new_hostname_to_set="$user_defined_hostname"
        else
            read -p 'Input hostname you want, then press Enter ' user_input_hostname
            new_hostname_to_set="$user_input_hostname"
        fi
        test -f /etc/hostname && echo "$new_hostname_to_set" > /etc/hostname
            test -f /etc/hostname && hostname -b -F /etc/hostname || hostname "$new_hostname_to_set"
        test -f /etc/sysconfig/network && sed -i "s/^HOSTNAME=.*.$/HOSTNAME=$new_hostname_to_set/g" /etc/sysconfig/network
    fi
    ipaddress_global_routing="`ip addr show scope global $(ip route | awk '/^default/ {print $NF}') | awk -F '[ /]+' '/global/ {print $3}'`"
    grep -v -E "($ipaddress_global_routing|$new_hostname_to_set)" /etc/hosts >/dev/null 2>&1 && echo "$ipaddress_global_routing $new_hostname_to_set" >> /etc/hosts
}

function yum_install_base_packages(){
    yum -y install vim wget curl perl unzip man man-pages man-pages-overrides bind-utils net-tools >/dev/null 2>&1
}

function yum_repository_config(){
    yum -y install http://dl.fedoraproject.org/pub/epel/6/x86_64/epel-release-6-8.noarch.rpm >/dev/null 2>&1

}

function yum_install_extra_packages(){
    yum info bash-completion >/dev/null 2>&1 && yum -y install bash-completion >/dev/null 2>&1
    yum -y update

}
function customized_commands(){
    # customized commands, alternatively, echo into .bashrc file as a function or alias
    cat >delsc.sh <<eof
#!/bin/bash
# delete all spaces and comments of specialized file, using with \$0 filename
[[ "\$1" == "" ]] && echo "delete all spaces and comments of specialized file, using with \$0 filename" && exit 1
if cat -A \$1 | grep '\^M\\\$' >/dev/null || file \$1 | grep "with CRLF line terminators" >/dev/null ; then
    which dos2unix >/dev/null 2>&1 || yum -q -y install dos2unix || apt-get -qq -y install dos2unix
    dos2unix \$1 >/dev/null
fi
if test -f \$1 && file \$1 | grep "XML" >/dev/null; then
    which tidy >/dev/null 2>&1 || yum -q -y install tidy || apt-get -qq -y install tidy
    tidy -quiet -asxml -xml -indent -wrap 1024 --hide-comments 1 \$1
elif test -f \$1; then
    grep -v \# \$1 | grep -v ^\; |grep -v ^$ | grep -v ^\ *$
fi
# Others:
# sed -e '/^#/d;/^$/d' \$1
# Refer: https://github.com/mysfitt/nocomment/blob/master/nocomment.sh
# grep -Ev '^\s*#|^//|^\s\*|^/\*|^\*/' \$1 | grep -Ev '^$|^\s+$'
eof
    chmod +x ./delsc.sh
    \cp delsc.sh /usr/local/bin/delsc
    rm -f ./delsc.sh
    SELINUX_STATE=$(cat "/selinux/enforce")
    [ -n "$SELINUX_STATE" -a -x /sbin/restorecon ] && /sbin/restorecon -r /usr/local/bin

}

function inject_ssh_key_for_root(){
    test ! -d /root/.ssh && ssh-keygen -N "" -f /root/.ssh/id_rsa
    test ! -f /root/.ssh/authorized_keys && cp /root/.ssh/id_rsa.pub /root/.ssh/authorized_keys
    cat >>/root/.ssh/authorized_keys<<eof
ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQCawuOgQup3Qc1OILytyH+u3S9te85ctEKTvzPtRjHfnEEOjpRS6v6/PsuDHplHO1PAm8cKbEZmqR9tg4mWSweosBYW7blUUB4yWfBu6cHAnJOZ7ADNWHHJHAYi8QFZd4SLAAKbf9J12Xrkw2qZkdUyTBVbm+Y8Ay9bHqGX7KKLhjt0FIqQHRizcvncBFHXbCTJWsAduj2i7GQ5vJ507+MgFl2ZTKD2BGX5m0Jq9z3NTJD7fEb2J6RxC9PypYjayXyQBhgACxaBrPXRdYVXmy3f3zRQ4/OmJvkgoSodB7fYL8tcUZWSoXFa33vdPlVlBYx91uuA6onvOXDnryo3frN1
ssh-rsa AAAAB3NzaC1yc2EAAAABJQAAAIEAumQ2srRwd9slaeYTdr/dGd0H4NzJ3uQdBQABTe/nhJsUFWVG3titj7JiOYjCb54dmpHoi4rAYIElwrolQttZSCDKTVjamnzXfbV8HvJapLLLJTdKraSXhiUkdS4D004uleMpaqhmgNxCLu7onesCCWQzsNw9Hgpx5Hicpko6Xh0=
eof
    SELINUX_STATE=$(cat "/selinux/enforce")
    [ -n "$SELINUX_STATE" -a -x /sbin/restorecon ] && /sbin/restorecon -r /root/.ssh

}

function bashrc_setting(){
    backup_single_file ~/.bashrc

    # history related
    # HISTTIMEFORMAT

    # PROMPT_COMMAND
    # Refer: http://dl528888.blog.51cto.com/2382721/1703059
    # Refer: http://www.tldp.org/HOWTO/Bash-Prompt-HOWTO/x264.html
    # TODO(Guodong Ding) a known issue, it will make user confused when a command line include a double quotes("), because is not a valid json any more
    #   like this "{"TIME":"2016-05-18 15:43:14", "HOSTNAME":"chris.51devops.com", "IP":"10.20.0.1", "LOGIN":"root", "USER":"root", "CMD":"export PROMPT_COMMAND='history 1|tail -1|sed "s/^[ ]\+[0-9]\+  //"|sed "s/^/{/"|sed "s/$/\"}/">> /var/log/command.log'"}"

    if ! grep HISTTIMEFORMAT ~/.bashrc && ! grep PROMPT_COMMAND;then
    cat >>~/.bashrc<<eof
export HISTTIMEFORMAT="\"TIME\":\"%F %T\", \"HOSTNAME\":\"$HOSTNAME\", \"IP\":\"\$(who -u am i 2>/dev/null| awk '{print \$NF}'|sed -e 's/[()]//g')\", \"LOGIN\":\"\$(who am i|awk '{print \$1}')\", \"USER\":\"\${USER}\", \"CMD\":\""
export PROMPT_COMMAND='history 1|tail -1|sed "s/^[ ]\+[0-9]\+  //"|sed "s/^/{/"|sed "s/$/\"}/">> /var/log/.command_history.log'
eof
    fi
}

function update_local_time(){
    if [[ ! `grep -a CST-8 /etc/localtime >/dev/null 2>&1` || ! `diff /etc/localtime /usr/share/zoneinfo/Asia/Shanghai >/dev/null 2>&1` ]]; then
        rm -rf /etc/localtime
        ln -s /usr/share/zoneinfo/Asia/Shanghai /etc/localtime
    fi
    ntpdate -u pool.ntp.org >/dev/null 2>&1 || ntpdate -u time.nist.gov >/dev/null 2>&1 || ntpdate -u time-nw.nist.gov >/dev/null 2>&1
    date
    cat >>/etc/rc.local<<eof
ntpdate -u pool.ntp.org || ntpdate -u time.nist.gov || ntpdate -u time-nw.nist.gov
hwclock -w
eof
    # Recommended do
    touch /etc/cron.daily/ntpdate
    chown -R --reference=/etc/cron.daily/logrotate /etc/cron.daily/ntpdate
    chmod -R --reference=/etc/cron.daily/logrotate /etc/cron.daily/ntpdate
    chcon -R --reference=/etc/cron.daily/logrotate /etc/cron.daily/ntpdate >/dev/null 2>&1
    cat >>/etc/cron.daily/ntpdate<<eof
ntpdate -u pool.ntp.org >/dev/null 2>&1 || ntpdate -u time.nist.gov >/dev/null 2>&1 || ntpdate -u time-nw.nist.gov >/dev/null 2>&1
hwclock -w
eof

}

function system_performance_tuning(){
    cp /etc/security/limits.conf /etc/security/limits.conf_origin_$(date +%Y%m%d%H%M%S)~
    cat >>/etc/security/limits.conf<<eof
# refer to the free inodes number, by "df -i" commands
* soft nofile 200000
* hard nofile 200000

eof

    cp /etc/sysctl.conf /etc/sysctl.conf_origin_$(date +%Y%m%d%H%M%S)~
    cat >/etc/sysctl.conf<<eof
fs.file-max = 808127
kernel.core_uses_pid = 1
kernel.hung_task_timeout_secs = 0
kernel.msgmax = 65536
kernel.msgmnb = 65536
kernel.sem = 250 32000 100 128
kernel.shmall = 4294967296
kernel.shmmax = 536870912
kernel.shmmax = 68719476736
kernel.shmmni = 4096
kernel.sysrq = 0
net.core.netdev_max_backlog = 262144
net.core.rmem_default = 8388608
net.core.rmem_max = 16777216
net.core.somaxconn = 262144
net.core.wmem_default = 8388608
net.core.wmem_max = 16777216
net.ipv4.conf.default.accept_source_route = 0
net.ipv4.conf.default.rp_filter = 1
net.ipv4.ip_forward = 0
net.ipv4.ip_local_port_range = 1024 65535
net.ipv4.tcp_fin_timeout = 1
net.ipv4.tcp_keepalive_time = 1200
net.ipv4.tcp_max_orphans = 3276800
net.ipv4.tcp_max_syn_backlog = 262144
net.ipv4.tcp_max_tw_buckets = 6000
net.ipv4.tcp_mem = 94500000 915000000 927000000
net.ipv4.tcp_rmem = 4096 87380 4194304
net.ipv4.tcp_sack = 1
net.ipv4.tcp_synack_retries = 5
net.ipv4.tcp_syncookies = 1
net.ipv4.tcp_syn_retries = 5
net.ipv4.tcp_timestamps = 0
net.ipv4.tcp_tw_recycle = 1
net.ipv4.tcp_tw_reuse = 1
net.ipv4.tcp_window_scaling = 1
net.ipv4.tcp_wmem = 4096 16384 4194304
vm.swappiness = 30
eof
    # TODO(Guodong Ding) OOM(sysctl -a | grep oom)

    # TODO(Guodong Ding) 5% reserved-blocks-percentage(tune2fs, dump2fs, man tune2fs)

    sysctl -p >/dev/null 2>&1

}

# TODO(Guodong Ding) noatime(man mount), fstab is only read by programs, and not written; it is the duty of the system \
#     administrator to properly create and maintain this file.
#     rw, suid, dev, exec, auto, nouser, async, and noatime

# TODO(Guodong Ding) more points


function ssh_config(){
    if grep "^#UseDNS" /etc/ssh/sshd_config >/dev/null 2>&1 && ! grep "UseDNS no" /etc/ssh/sshd_config >/dev/null 2>&1; then
        cp /etc/ssh/sshd_config /etc/ssh/sshd_config_origin_$(date +%Y%m%d%H%M%S)~
        sed -i "s/^#UseDNS.*.$/UseDNS no/g" /etc/ssh/sshd_config
        #
        sed -i 's/GSSAPIAuthentication yes/GSSAPIAuthentication no/' /etc/ssh/sshd_config
        service sshd restart
    fi

}

# TODO(Guodong Ding) Reducing Disk IO By Mounting Partitions With noatime
    # Refer: https://www.howtoforge.com/reducing-disk-io-by-mounting-partitions-with-noatime
    # Refer: man 8 mount

function add_user_as_user_defined(){
    if test -z ${user_defined_username}; then
        return 0
    else
        useradd ${user_defined_username}
        test -d /etc/sudoers.d && echo "$user_defined_username ALL=(ALL) NOPASSWD: ALL" > /etc/sudoers.d/user_$user_defined_username.conf
    fi

}

function initialize(){
    check_network_connectivity
    check_name_resolve
    set_hostname_fqdn_format
    yum_install_base_packages
    yum_repository_config
    yum_install_extra_packages
    customized_commands
    inject_ssh_key_for_root
    bashrc_setting
    update_local_time
    system_performance_tuning
    ssh_config
}
function main(){
    lock_filename="lock_$$_$RANDOM"
#    lock_filename_full_path="/var/lock/subsys/$lock_filename"
    lock_filename_full_path="/var/lock/$lock_filename"
    if ( set -o noclobber; echo "$$" > "$lock_filename_full_path") 2> /dev/null;then
        trap 'rm -f "$lock_filename_full_path"; exit $?' INT TERM EXIT
        # Just a test for call itself, comment it
         if [[ $# -ne 1 ]]; then
            [ ! -x ${WORKDIR}/`basename $0` ] && chmod +x ${WORKDIR}/`basename $0`
            test -z ${header} || echo_b "$header"
            ${WORKDIR}/`basename $0` initialize
            exit 0
         fi
        case $1 in
            initialize)
                initialize
                ;;
            help|*)
                test -z ${header} || echo_b "$header"
                echo "Usage: $0 {initialize} with $0 itself"
                exit 1
                ;;
        esac

        rm -f "$lock_filename_full_path"
        trap - INT TERM EXIT
    else
        echo "Failed to acquire lock: $lock_filename_full_path"
        echo "held by $(cat ${lock_filename_full_path})"
fi

}

main $@

# debug option
#${_XTRACE_FUNCTIONS}

