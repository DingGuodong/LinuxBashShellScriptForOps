#!/bin/bash
# Created by PyCharm.
# File Name:              LinuxBashShellScriptForOps:nginx-install-update.sh
# Version:                0.0.1
# Author:                 Guodong
# Author Email:           dgdenterprise@gmail.com
# URL:                    https://github.com/DingGuodong/LinuxBashShellScriptForOps
# Download URL:           https://github.com/DingGuodong/LinuxBashShellScriptForOps/tarball/master
# Create Date:            2018/11/15
# Create Time:            15:54
# Description:            install or update nginx server with Bash Shell Scripting
# Long Description:       The reason for writing this script in bash shell language instead of writing it in Python is
#                         because it is not pythonic at all
# Usage:                  sudo bash $0
# References:
# Prerequisites:          []
# Development Status:     3 - Alpha, 5 - Production/Stable
# Environment:            Console
# Intended Audience:      System Administrators, Developers, End Users/Desktop
# License:                Freeware, Freely Distributable
# Natural Language:       English, Chinese (Simplified)
# Operating System:       POSIX :: Linux
# Programming Language:   GNU bash :: 4+
# Topic:                  Utilities

#set -e

NGINX_SOURCE_LATEST_VERSION="nginx-1.14.2"
PCRE_SOURCE_LATEST_VERSION="pcre-8.43"
ZLIB_SOURCE_LATEST_VERSION="zlib-1.2.11"
OPENSSL_SOURCE_LATEST_VERSION="openssl-1.1.1b"


function echo_r (){
    # Color red: Error, Failed
    [[ $# -ne 1 ]] && return 1
    echo -e "\033[31m$1\033[0m"
}
function echo_g (){
    # Color green: Success
    [[ $# -ne 1 ]] && return 1
    echo -e "\033[32m$1\033[0m"
}
function echo_y (){
    # Color yellow: Warning
    [[ $# -ne 1 ]] && return 1
    echo -e "\033[33m$1\033[0m"
}
function echo_b (){
    # Color blue: Debug Level 1
    [[ $# -ne 1 ]] && return 1
    echo -e "\033[34m$1\033[0m"
}

function echo_p (){
    # Color purple,magenta: Debug Level 2
    [[ $# -ne 1 ]] && return 1
    echo -e "\033[35m$1\033[0m"
}

function echo_c (){
    # Color cyan: friendly prompt, Level 1
    [[ $# -ne 1 ]] && return 1
    echo -e "\033[36m$1\033[0m"
}


function confirm_continue(){
    echo "Is this ok? "
    read -n 1 -r -p "Enter the y or Y to continue:" user_answer  # read -n1 -r -p "Press any key to continue..." key
    if [[ "${user_answer}" != "y" ]] && [[ "${user_answer}" != "Y" ]]; then
        echo -e "\n\nExiting on user cancel."  # exiting because "Download Only" specified
        exit 1
    else
        echo
    fi
}


WORKDIR="/tmp/.install_nginx_from_source"
[[ ! -d ${WORKDIR} ]] && mkdir ${WORKDIR}
[[ -d ${WORKDIR} ]] && cd ${WORKDIR}


function check_ports(){
    if netstat -ntl | awk '{if($4 ~ /:80$/ ) print}' | grep ':80'; then
        echo_y "`date '+%Y-%m-%d %H:%M:%S.%N'` WARNING: port 80 in use"
        confirm_continue
    elif netstat -ntl | awk '{if($4 ~ /:443/ ) print}' | grep ':443'; then
        echo_y "`date '+%Y-%m-%d %H:%M:%S.%N'` WARNING: port 443 in use"
        confirm_continue
    else
        echo_g "`date '+%Y-%m-%d %H:%M:%S.%N'` Passed: port 80/443 not in use"
    fi
}


function compare_version(){
    # Compare the version number with `sort -V` or directly remove the dot before comparison
    if test $(echo $@ | tr " " "\n"| sort -rV | head -1) == $1; then
        return 0
    else
        return 1
    fi
}

function can_install_update(){
    if which nginx >/dev/null 2>&1; then
        current_version=`/usr/sbin/nginx -V |& grep "nginx\ version" | awk -F"/" '{print$NF}'`
        latest_version=`echo ${NGINX_SOURCE_LATEST_VERSION}| awk -F"-" '{print$NF}'`
        if compare_version ${current_version} ${latest_version}; then
            echo_g "`date '+%Y-%m-%d %H:%M:%S.%N'` check passed and skipped!"
            exit 0
        else
            echo_c "`date '+%Y-%m-%d %H:%M:%S.%N'` nginx can be upgrade!"
            check_ports
            return 1
        fi
    else
        echo_c "`date '+%Y-%m-%d %H:%M:%S.%N'` nginx can be install!"
        check_ports
        return 0
    fi
}

function add_users(){
    if ! grep ^www: /etc/passwd >/dev/null 2>&1; then
        echo_b "`date '+%Y-%m-%d %H:%M:%S.%N'` adding group and user ..."
        groupadd -r www
        useradd -r -g www www -c "Web user" -d /dev/null -s /sbin/nologin
    fi
}

function is_nginx_installed(){
    if test -d /usr/local/nginx && test -x /usr/local/nginx/sbin/nginx || test -f ${HOME}/.nginx_installed; then
        # installed
        return 0  # return will save result to $?
    else
        # not installed by source or not installed
        retrun 1  # numeric argument can be 0, 1, 2, ...
    fi
}

function download_source_packages(){
    echo_b "`date '+%Y-%m-%d %H:%M:%S.%N'` downloading packages ..."
    # http://nchc.dl.sourceforge.net/project/pcre/pcre/8.39/pcre-8.39.tar.gz
    [[ ! -f ${WORKDIR}/${NGINX_SOURCE_LATEST_VERSION}.tar.gz ]] && wget -c http://nginx.org/download/${NGINX_SOURCE_LATEST_VERSION}.tar.gz  >/dev/null 2>&1 # http://nginx.org/en/download.html
    [[ ! -f ${WORKDIR}/${PCRE_SOURCE_LATEST_VERSION}.tar.gz ]] && wget -c https://ftp.pcre.org/pub/pcre/${PCRE_SOURCE_LATEST_VERSION}.tar.gz  >/dev/null 2>&1 # ftp://ftp.csx.cam.ac.uk/pub/software/programming/pcre/
    [[ ! -f ${WORKDIR}/${ZLIB_SOURCE_LATEST_VERSION}.tar.gz ]] && wget -c http://zlib.net/${ZLIB_SOURCE_LATEST_VERSION}.tar.gz  >/dev/null 2>&1 # http://zlib.net/
    [[ ! -f ${WORKDIR}/${OPENSSL_SOURCE_LATEST_VERSION}.tar.gz ]] && wget -c https://www.openssl.org/source/${OPENSSL_SOURCE_LATEST_VERSION}.tar.gz  >/dev/null 2>&1 # https://www.openssl.org/source/
}

function install_base(){
    # Completing Preinstallation Tasks
    echo_b "`date '+%Y-%m-%d %H:%M:%S.%N'` install base packages ..."
    apt-get -y update >/dev/null 2>&1 || yum makecache >/dev/null 2>&1
    apt-get -y install gcc g++ make >/dev/null 2>&1 || yum install -y gcc gcc-c++ make >/dev/null 2>&1
}

function compile_nginx_source(){
    echo_b "`date '+%Y-%m-%d %H:%M:%S.%N'` compile nginx and install nginx ..."
    tar zxf ${NGINX_SOURCE_LATEST_VERSION}.tar.gz
    tar zxf ${PCRE_SOURCE_LATEST_VERSION}.tar.gz
    tar zxf ${ZLIB_SOURCE_LATEST_VERSION}.tar.gz
    tar zxf ${OPENSSL_SOURCE_LATEST_VERSION}.tar.gz

    cd ${WORKDIR}/${NGINX_SOURCE_LATEST_VERSION}
    ./configure --prefix=/usr/local/nginx \
        --with-http_ssl_module \
        --with-stream \
        --user=www --group=www \
        --with-pcre-jit \
        --with-pcre=${WORKDIR}/${PCRE_SOURCE_LATEST_VERSION} \
        --with-zlib=${WORKDIR}/${ZLIB_SOURCE_LATEST_VERSION} \
        --with-openssl=${WORKDIR}/${OPENSSL_SOURCE_LATEST_VERSION} >/dev/null 2>&1
    make >/dev/null 2>&1 && make install >/dev/null 2>&1
    cd
}

function post_install(){
    echo_b "`date '+%Y-%m-%d %H:%M:%S.%N'` pos-install nginx ..."
    [[ -h /usr/sbin/nginx ]] || ln -s /usr/local/nginx/sbin/nginx /usr/sbin/nginx

    nginx -V
    nginx -t >/dev/null 2>&1

    if [[ -f /usr/local/nginx/logs/nginx.pid ]] && kill -0 `cat /usr/local/nginx/logs/nginx.pid` >/dev/null 2>&1 ; then
        nginx -s stop && nginx
    else
        nginx
    fi

    netstat -lnpt | grep nginx
}

function optimize_security_rules(){
    # Checking Resource Limits
    # https://docs.oracle.com/cd/B28359_01/install.111/b32002/pre_install.htm#LADBI246
    # https://docs.oracle.com/en/database/oracle/oracle-database/18/ladbi/checking-resource-limits-for-oracle-software-installation-users.html#GUID-293874BD-8069-470F-BEBF-A77C06618D5A
    cp /etc/security/limits.d/www.conf /etc/security/limits.d/www.conf$(date +%Y%m%d%H%M%S)~
    tee /etc/security/limits.d/www.conf<<'eof'
www              soft    nproc   2047
www              hard    nproc   16384
www              soft    nofile  1024
www              hard    nofile  65536
eof

#ulimit -Sn # Check the soft and hard limits for the file descriptor setting.
#ulimit -Hn
#ulimit -Su # Check the soft and hard limits for the number of processes available to a user.
#ulimit -Hu
#ulimit -Ss # Check the soft limit for the stack setting.
#ulimit -Hs
}

function optimize_kernel_parameters(){
    # Configuring Kernel Parameters for Linux
    # http://docs.oracle.com/cd/B28359_01/install.111/b32002/pre_install.htm#LADBI246
    # https://docs.oracle.com/en/database/oracle/oracle-database/18/ladbi/minimum-parameter-settings-for-installation.html#GUID-CDEB89D1-4D48-41D9-9AC2-6AD9B0E944E3
    # https://docs.oracle.com/en/database/oracle/oracle-database/18/ladbi/changing-kernel-parameter-values.html#GUID-FB0CC366-61C9-4AA2-9BE7-233EB6810A31
    cp /etc/sysctl.conf /etc/sysctl.conf$(date +%Y%m%d%H%M%S)~
    cat >/etc/sysctl.conf<<eof
# http://docs.oracle.com/cd/B28359_01/install.111/b32002/pre_install.htm#LADBI246
fs.aio-max-nr = 1048576
fs.file-max = 6815744
kernel.core_uses_pid = 1
kernel.hung_task_timeout_secs = 0
kernel.msgmax = 65536
kernel.msgmnb = 65536
kernel.sem = 250 32000 100 128
kernel.shmall gc_stale_time= 4294967295
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
net.ipv4.ip_local_port_range = 9000 65500
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
vm.swappiness = 0
m.max_map_count=262144
eof
    sysctl -p

    test -x /etc/init.d/procps && (service procps start || systemctl start systemd-sysctl.service)

    if test $(uname -r | awk -F'.' '{print$1}') -gt 3; then
        # https://www.bufferbloat.net/projects/codel/wiki/
        echo_y "if your kernel version >3, net.core.default_qdisc maybe need to configured."
    fi
}

function generate_config_file(){
    echo_b "`date '+%Y-%m-%d %H:%M:%S.%N'` generating nginx config file ..."
    # /var/lib/python/python3.5_installed
    if ! -f ${HOME}/.nginx_installed ; then
        tee /usr/local/nginx/conf/nginx.conf<<-'eof'
user www;
worker_processes  auto;
worker_rlimit_nofile 200000;
error_log logs/error.log notice;
pid        logs/nginx.pid;
events {
    use epoll;
    worker_connections  51200;
    multi_accept on;
}
http {
    include        mime.types;
    client_body_timeout 10s;
    client_max_body_size  128M;
    default_type   application/octet-stream;
    sendfile       on;
    send_timeout   2s;
    tcp_nodelay    on;
    tcp_nopush     on;
    keepalive_timeout  65;
    keepalive_requests 200000;
    reset_timedout_connection on;
    server_tokens off;
    gzip  on;
    gzip_min_length 10240;
    gzip_proxied expired no-cache no-store private auth;
    gzip_types text/plain text/css text/xml text/javascript application/x-javascript application/xml;
    gzip_disable "MSIE [1-6]\.";
    gzip_vary on;
    access_log     off;
    open_file_cache max=200000 inactive=20s;
    open_file_cache_valid    30s;
    open_file_cache_min_uses 2;
    open_file_cache_errors   on;
    log_format  main  '$remote_addr - $remote_user [$time_local] "$request" '
              '$status $body_bytes_sent "$http_referer" '
              '"$http_user_agent" "$http_x_forwarded_for"';
include conf.d/*.conf;
}
eof
        test -d /usr/local/nginx/conf/conf.d && test ! -h /usr/local/nginx/conf/conf.d && rm -r /usr/local/nginx/conf/conf.d/
        mkdir -p /usr/local/nginx/conf/vhost
        ln -s /usr/local/nginx/conf/vhost /usr/local/nginx/conf/conf.d
        tee /usr/local/nginx/conf/vhost/default.conf<<-eof
server {
        listen       80;
        server_name  localhost;

        access_log  logs/http_default.access.log  main;

        location / {
            root   html;
            index  index.html index.htm;
        }

        error_page   500 502 503 504  /50x.html;
        location = /50x.html {
            root   html;
        }

    }
eof
        wget http://nginx.org/favicon.ico -O /usr/local/nginx/html/favicon.ico
        nginx -t && sudo nginx -s reload
    fi
}

function clean(){
    echo_b "`date '+%Y-%m-%d %H:%M:%S.%N'` clean installation ..."
    test ! -f ${HOME}/.nginx_installed && touch ${HOME}/.nginx_installed
    # cd && rm -rf ${WORKDIR}
    echo_g "`date '+%Y-%m-%d %H:%M:%S.%N'` nginx installation or update finished successfully!"
}

function install_nginx(){
    if can_install_update; then # install
        echo_c "`date '+%Y-%m-%d %H:%M:%S.%N'` begin install nginx ..."
        install_base
        add_users
        download_source_packages
        compile_nginx_source
        post_install
        if ! is_nginx_installed; then
            generate_config_file
        fi
        clean
    else # update
        echo_c "`date '+%Y-%m-%d %H:%M:%S.%N'` begin update nginx ..."
        download_source_packages
        compile_nginx_source
        post_install
        clean
    fi
}

function main(){
    install_nginx
}

main

#set +e
