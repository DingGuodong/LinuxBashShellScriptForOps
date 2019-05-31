#!/usr/bin/env bash
# Created by PyCharm.
# File Name:              LinuxBashShellScriptForOps:php7-install-update.sh
# Version:                0.0.1
# Author:                 Guodong
# Author Email:           dgdenterprise@gmail.com
# URL:                    https://github.com/DingGuodong/LinuxBashShellScriptForOps
# Download URL:           https://github.com/DingGuodong/LinuxBashShellScriptForOps/tarball/master
# Create Date:            2018/11/19
# Create Time:            14:04
# Description:            
# Long Description:       
# Usage:                  
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

set -e

PHP7_VERSION=7.2.12
PHP7_SOURCE_LATEST_VERSION=php-${PHP7_VERSION}

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


WORKDIR="/tmp/.install_php7_from_source"
[[ ! -d ${WORKDIR} ]] && mkdir ${WORKDIR}
[[ -d ${WORKDIR} ]] && cd ${WORKDIR}

function compare_version(){
    # Compare the version number with `sort -V` or directly remove the dot before comparison
    if test $(echo $@ | tr " " "\n"| sort -rV | head -1) == $1; then
        return 0
    else
        return 1
    fi
}

function can_install_update(){
    pass
}

function add_users(){
    if ! grep ^www: /etc/passwd >/dev/null 2>&1; then
        groupadd -r www
        useradd -r -g www www -c "Web user" -d /dev/null -s /sbin/nologin
    fi
}

function is_php7_installed(){
    if test -d /usr/local/nginx && test -x /usr/local/nginx/sbin/nginx || test -f ${HOME}/.nginx_installed; then
        # installed
        return 0  # return will save result to $?
    else
        # not installed by source or not installed
        retrun 1  # numeric argument can be 0, 1, 2, ...
    fi
}

function download_source_packages(){
    [[ ! -f ${WORKDIR}/php-${PHP7_VERSION}.tar.gz ]] && wget -c http://cn.php.net/distributions/php-${PHP7_VERSION}.tar.gz
}

function install_base(){
    # Completing Preinstallation Tasks
    sudo apt install -y build-essential autoconf libjpeg-turbo8-dev libpng-dev libfreetype6-dev libxslt1-dev libsystemd-dev libldap2-dev
}

function compile_php7_source(){
    tar zxf php-${PHP7_VERSION}.tar.gz

    cd ${WORKDIR}/${PHP7_SOURCE_LATEST_VERSION}
    ./configure --prefix=/usr/local/php7 --with-config-file-path=/usr/local/php7/etc --with-config-file-scan-dir=/usr/local/php7/conf.d --enable-fpm --with-fpm-user=www --with-fpm-group=www  --with-mysqli=mysqlnd --with-pdo-mysql=mysqlnd --with-iconv-dir --with-freetype-dir --with-jpeg-dir --with-png-dir --with-zlib --with-libxml-dir --enable-xml --disable-rpath --enable-bcmath --enable-shmop --enable-sysvsem --with-fpm-systemd --enable-inline-optimization --with-curl --enable-mbregex --enable-mbstring --enable-ftp --with-gd --with-openssl --with-mhash --enable-pcntl --enable-sockets --with-xmlrpc --with-libzip --enable-soap --with-gettext --enable-fileinfo --enable-opcache --enable-intl --with-xsl --with-ldap
    make >/dev/null
    sudo make install >/dev/null

}

function post_install(){
    sudo cp php.ini-production /usr/local/php7/etc/php.ini
    grep include_path /usr/local/php7/etc/php.ini
    sudo sed -i 's@;include_path = ".:/php/includes"@include_path = ".:/usr/local/php7/lib/php"@g' /usr/local/php7/etc/php.ini
    # sudo cp sapi/fpm/init.d.php-fpm /etc/init.d/php7-fpm
    # sudo chmod +x /etc/init.d/php7-fpm
    ls sapi/fpm/php-fpm.service
    sudo cp sapi/fpm/php-fpm.service /lib/systemd/system/php7-fpm.service
    sudo systemctl enable php7-fpm.service
    sudo systemctl daemon-reload
    sudo cp sapi/fpm/php-fpm.conf /usr/local/php7/etc/php-fpm.conf
    grep -v \; /usr/local/php7/etc/php-fpm.conf | grep -v ^$
    grep -v \; /usr/local/php7/etc/php-fpm.d/www.conf.default | grep -v ^$
    grep -v \; /usr/local/php7/etc/php-fpm.d/www.conf.default | grep -v ^$ | sudo tee /usr/local/php7/etc/php-fpm.d/www.conf
    cat /usr/local/php7/etc/php-fpm.d/www.conf
    sudo sed -i 's/listen = 127.0.0.1:9000/listen = 127.0.0.1:9001/g' /usr/local/php7/etc/php-fpm.d/www.conf
    cat /usr/local/php7/etc/php-fpm.d/www.conf

    sudo systemctl start php7-fpm.service
    systemctl status php7-fpm.service
    netstat -anop | grep 9001

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
    grep post_max_size /usr/local/php7/etc/php.ini
    grep max_input_time /usr/local/php7/etc/php.ini
    grep date.timezone /usr/local/php7/etc/php.ini
    grep max_execution_time /usr/local/php7/etc/php.ini
    sudo sed -i 's/post_max_size = 8M/post_max_size = 16M/g' /usr/local/php7/etc/php.ini
    sudo sed -i 's/max_input_time = 60/max_input_time = 300/g' /usr/local/php7/etc/php.ini
    sudo sed -i 's@;date.timezone =@date.timezone = Asia/Shanghai@g' /usr/local/php7/etc/php.ini
    sudo sed -i 's/max_execution_time = 30/max_execution_time = 300/g' /usr/local/php7/etc/php.ini
    sudo sed -i 's/;always_populate_raw_post_data = -1/always_populate_raw_post_data = -1/g' /usr/local/php7/etc/php.ini
    sudo systemctl restart php7-fpm.service
    systemctl status php7-fpm.service

}

function clean(){
    test ! -f ${HOME}/.php7_installed && touch ${HOME}/.php7_installed
    cd && rm -rf ${WORKDIR}
    echo_g "PHP7 installation or update finished successfully!"
}

function install_php7(){
    can_install_update
    install_base
    add_users
    download_source_packages
    compile_php7_source
    post_install
    if ! is_php7_installed; then
        generate_config_file
    fi
    clean
}

function main(){
    install_php7
}

main

set +e