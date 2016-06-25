#!/bin/bash

# Name: doDeploy.sh
#Execute this shell script to deploy Java projects built by Maven automatically on remote hosts.

# debug option
DEBUG=false
#DEBUG=true

if ${DEBUG} ; then
    old_PS4=$PS4
#    export PS4='+${BASH_SOURCE}:${LINENO}:${FUNCNAME[0]}: '
    export PS4='+${LINENO}: ${FUNCNAME[0]}: ' # if there is only one bash script, do not display ${BASH_SOURCE}
    _XTRACE_FUNCTIONS=$(set +o | grep xtrace)
    set -o xtrace
fi

# define user friendly messages
header="
Function: Execute this shell script to deploy Java projects built by Maven automatically on remote hosts.
License: Open source software
"

# user defined variables
# Where to get source code
user_defined_project_clone_depends="ssh://git@git.huntor.cn:18082/core/business-service-base.git"
user_defined_project_clone="ssh://git@git.huntor.cn:18082/core/business-service-core.git"
# TODO(Guodong Ding) do deploy once time with multi-hosts support, try using 'for + deploy'
user_defined_deploy_target_host_ip="10.6.28.135" # this is a mandatory field, and must be same as the first ip in $user_defined_deploy_targets_host_ip_list
user_defined_deploy_targets_host_ip_list="10.6.28.135 10.6.28.28"
#user_defined_project_top_directory_to_target_host="/data/docker/business-service/bs-core-01"
#user_defined_docker_container_name="bs-core-01"
user_defined_project_top_directory_to_target_host="/tmp/deploy_test_target"
user_defined_docker_container_name="testcontainer" # if you using a docker container other than a startup script located in sourcecode/bin/startup.sh, then set this to docker container name
user_defined_project_conf_directory="backup" # if you do NOT want to use configurations from deploy target, you should set this variable to where pointed to config files
user_defined_skip_check_network_and_resolver="true" # if system administrator disable ICMP protocol, set this any content but not null
# Setting how many days do you want save old releases, default is 10 days
save_old_releases_for_days=10
# end define variables

# pretreatment
test -z ${user_defined_project_clone_depends} || project_clone_target_depends_1="`echo ${user_defined_project_clone_depends} | awk -F '[/.]+' '{ print $(NF-1)}'`"
project_clone_target="`echo ${user_defined_project_clone} | awk -F '[/.]+' '{ print $(NF-1)}'`"
project_clone_repository_name=${project_clone_target}
deployment_mode=""
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
    # Color purple,magenta: Debug Level 2
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
    echo "WARNING: Running as a non-root user, \"$LOGNAME\". Functionality may be unavailable. Only root can use some commands or options"
fi

function command_exists() {
    # which "$@" >/dev/null 2>&1
    command -v "$@" >/dev/null 2>&1
}

function check_command_can_be_execute(){
    [ $# -ne 1 ] && return 1
    command_exists $1
}

function check_network_connectivity(){
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
        echo
    fi
}

function check_name_resolve(){
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
        echo
        return 0
    fi
}

function check_ssh_can_be_connect(){
    [ $# -ne 1 ] && return 1
    echo_b "Check if can ssh to remote host $1 ... "
    check_command_can_be_execute ssh || return 1
    # TODO(Guodong Ding) ssh can connect to remote host by using /etc/ssh/ssh_host_rsa_key or ~/.ssh/id_rsa
    ssh -i /etc/ssh/ssh_host_rsa_key -p 22 -oStrictHostKeyChecking=no root@$1 "uname -a >/dev/null 2>&1"
    retval=$?
    if [ ${retval} -ne 0 ] ; then
        echo_r "Check ssh to remote host $1 failed! "
        exit 1
    else
        echo_g "Check ssh to remote host $1 successfully! "
    fi
}

function check_other_dependencies() {
    echo_b "Checking other dependencies for deploy procedure... "

    echo_b "\tChecking user customized variables..."
    # Refer:
    # if [ -z ${var+x} ]; then
    #     echo "var is unset"; else echo "var is set to '$var'"
    # fi
    # if [ "$var x" = " x" ]; then
    #     echo "var is empty"; else echo "var is set to '$var'"
    # fi
    # if [ -z $var ]; then
    #     echo "var is empty"; else echo "var is set to '$var'"
    # fi
    if [[ -z ${user_defined_project_clone} ]]; then
        echo_r "Error: user_defined_project_clone is undefined! "
        exit 1
    fi

    # Note: test command is strongly typed, can recognize string type and integer type
    if test ! -z "$user_defined_deploy_target_host_ip" -a ! -z "$user_defined_deploy_targets_host_ip_list" ; then
        user_defined_deploy_targets_host_first_ip_in_list="`echo "$user_defined_deploy_targets_host_ip_list" | awk -F ' ' '{ print $1 }'`"
        if test "$user_defined_deploy_target_host_ip" = "$user_defined_deploy_targets_host_first_ip_in_list" -a "$deployment_mode" = "0" ; then
            echo_g "Run this shell script in multi-deployment mode, deploy to a group of hosts."
            saved_IFS=$IFS
            IFS=' '
            for ipaddress in ${user_defined_deploy_targets_host_ip_list}; do
                check_ssh_can_be_connect ${ipaddress}
            done
            IFS=${saved_IFS}
        else
            echo_r "$user_defined_deploy_targets_host_ip_list is not equal to $user_defined_deploy_target_host_ip, this is a must! "
            exit 1
        fi
    elif test ! -z "$user_defined_deploy_target_host_ip" -a -z "$user_defined_deploy_targets_host_ip_list" -a "$deployment_mode" = "1" ;then
        echo_g "Run this shell script in standalone-deployment mode, deploy to single host."
    elif test -z "$user_defined_deploy_target_host_ip" -a -z "$user_defined_deploy_targets_host_ip_list" ;then
        echo_r "Error: both user_defined_deploy_target_host_ip and user_defined_deploy_targets_host_ip_list is undefined! "
        exit 1
    else
        echo_r "Error: bad user defined parameters, please fix it and try again! "
        exit 1
    fi
    if [[ -z ${user_defined_project_top_directory_to_target_host} ]]; then
        echo_r "Error: user_defined_project_top_directory_to_target_host is undefined! "
        exit 1
    fi

    if test -z ${user_defined_project_conf_directory}; then
        echo_y "Warning: user defined project conf directory is not defined! "
    fi

    echo_g "\tChecking user customized and defined variables passed! "

    echo_b "\tChecking disk space available..."
    disk_space_available=`df ${WORKDIR} | tail -n1 | awk '{print $(NF-2)}'`
    if [[ ${disk_space_available} -lt 2097152 ]]; then
        echo_y "Warning: Disk space of $WORKDIR is smaller than 2GB"
        #exit 1
    else
        echo_g "\tChecking disk space available passed! "
    fi

    echo_g "All required dependencies check passed! "
    echo

}

function setDirectoryStructureOnLocalHost() {
    if [ -f ${WORKDIR}/.capistrano_ds_lock ];then
        echo_g "Set directory structure has been done, skipping. "
        return
    fi
    echo_b "Setting directory structure... "
    # learn from capistrano
    # Refer: http://capistranorb.com/documentation/getting-started/structure/
    # Refer: http://capistranorb.com/documentation/getting-started/structure/#

    # ├── current -> /var/www/my_app_name/releases/20150120114500/
    # ├── releases
    # │   ├── 20150080072500
    # │   ├── 20150090083000
    # │   ├── 20150100093500
    # │   ├── 20150110104000
    # │   └── 20150120114500
    # ├── repo
    # │   └── <VCS related data>
    # ├── revisions.log
    # └── shared
    #     └── <linked_files and linked_dirs>

    # current is a symlink pointing to the latest release. This symlink is updated at the end of a successful deployment. If the deployment fails in any step the current symlink still points to the old release.
    # releases holds all deployments in a timestamped folder. These folders are the target of the current symlink.
    # repo holds the version control system configured. In case of a git repository the content will be a raw git repository (e.g. objects, refs, etc.).
    # revisions.log is used to log every deploy or rollback. Each entry is timestamped and the executing user (username from local machine) is listed. Depending on your VCS data like branch names or revision numbers are listed as well.
    # shared contains the linked_files and linked_dirs which are symlinked into each release. This data persists across deployments and releases. It should be used for things like database configuration files and static and persistent user storage handed over from one release to the next.
    # The application is completely contained within the path of :deploy_to. If you plan on deploying multiple applications to the same server, simply choose a different :deploy_to path.

    # Check directories for deploy
    [ ! -d ${WORKDIR}/release ] && mkdir ${WORKDIR}/release
    [ ! -d ${WORKDIR}/repository ] && mkdir ${WORKDIR}/repository
    [ ! -d ${WORKDIR}/share ] && mkdir ${WORKDIR}/share
    # end directories structure

    # Additional directories structure for full deploy operation
    # for backup remote host config file
    [ ! -d ${WORKDIR}/backup ] && mkdir ${WORKDIR}/backup

    # set a directories structure lock
    touch ${WORKDIR}/.capistrano_ds_lock
    echo_g "Set directory structure successfully! "
    echo
}

function clean_old_releases(){
    echo_b "Clean old releases... "
    save_days=${save_old_releases_for_days:-10}
    if [ ! -d ${WORKDIR}/release ]; then
        echo_b "Can NOT find release directory, skipping . "
        return
    fi
    need_clean=$(find ${WORKDIR}/release -mtime +${save_days} -exec ls '{}' \;)
    if [ ! -z ${need_clean} ]; then
        echo_c "Expired releases found and will be removed from project! "
        find ${WORKDIR}/release -mtime +${save_days} -exec rm -rf '{}' \;
        if [ $? -eq 0 ]; then
            echo_g "Expired releases have removed from project! "
        else
            echo_r "Can NOT remove expired releases, please feel free to alter to administrators. "
        fi
    else
        echo_g "All releases are not expired, skipping. "
    fi

}

function clean_old_logs(){
    echo_b "Clean old logs... "
    save_days=${save_old_releases_for_days:-10}
    need_clean=$(find ${WORKDIR}/ -name "*.log" -mtime +${save_days} -exec ls '{}' \;)
    if [ ! -z ${need_clean} ]; then
        echo_c "Expired releases found and will be removed from project! "
        find -L ${WORKDIR}/ -maxdepth 1 -name "*.log" -a ! -name "^." -mtime +${save_days} -exec rm -rf '{}' \;
        if [ $? -eq 0 ]; then
            echo_g "Expired logs have removed from project! "
        else
            echo_r "Can NOT remove expired logs, please feel free to alter to administrators. "
        fi
    else
        echo_g "All logs are not expired, skipping. "
    fi

}

# git_project_clone repository branch
function git_project_clone(){
    set -o errexit
    [ $# -ge 1 ] && project_clone_repository="$1"
    project_clone_repository_name="`echo ${project_clone_repository} | awk -F '[/.]+' '{ print $(NF-1)}'`"
    project_clone_directory=${WORKDIR}/repository/${project_clone_repository_name}
    if test -n $2; then
        branch="$2"
    else
        branch="develop"
    fi
    if test ! -d ${project_clone_directory}; then
        echo_b "git clone from $project_clone_repository"
        # git clone git@github.com:name/app.git -b master
        git clone ${project_clone_repository} ${project_clone_directory} >>${WORKDIR}/git_$(date +%Y%m%d)_$$.log 2>&1
            # TODO(Guodong Ding) get branch names or revision numbers from VCS data

        cd ${project_clone_directory}
        git checkout ${branch} >>${WORKDIR}/git_$(date +%Y%m%d)_$$.log 2>&1
        cd ..
        echo_g "git clone from $project_clone_repository successfully! "
    else
        echo_b "git pull from $project_clone_repository"
        cd ${project_clone_directory}
        git pull >>${WORKDIR}/git_$(date +%Y%m%d)_$$.log 2>&1
        git checkout ${branch} >>${WORKDIR}/git_$(date +%Y%m%d)_$$.log 2>&1
        # TODO(Guodong Ding) get branch names or revision numbers from VCS data
        cd ..
        echo_g "git pull from $project_clone_repository successfully! "
    fi
    set +o errexit
}

function maven_build_project_deprecated(){
    set -o errexit
    echo_b "Do mvn build java project... "
    check_command_can_be_execute mvn
    [ $# -ge 1 ] && project_clone_repository="$1"
    project_clone_repository_name="`echo ${project_clone_repository} | awk -F '[/.]+' '{ print $(NF-1)}'`"
    project_clone_directory=${WORKDIR}/repository/${project_clone_repository_name}
    cd ${project_clone_directory}
    mvn install >>${WORKDIR}/mvn_build_$(date +%Y%m%d)_$$.log 2>&1
    mvn clean package >>${WORKDIR}/mvn_build_$(date +%Y%m%d)_$$.log 2>&1
    cd ..
    echo_g "Do mvn build java project finished with exit code 0! "
    set +o errexit
}

function maven_build_project(){
    echo_b "Do mvn build java project for `echo $1 | awk -F '[/.]+' '{ print $(NF-1)}'`... "
    check_command_can_be_execute mvn
    [ $# -ge 1 ] && project_clone_repository="$1"
    project_clone_repository_name="`echo ${project_clone_repository} | awk -F '[/.]+' '{ print $(NF-1)}'`"
    project_clone_directory=${WORKDIR}/repository/${project_clone_repository_name}

    cd ${project_clone_directory}
    mvn install >>${WORKDIR}/mvn_build_$(date +%Y%m%d)_$$.log 2>&1
    retval=$?
    if [ ${retval} -ne 0 ] ; then
        echo_r "mvn install failed! More details refer to ${WORKDIR}/mvn_build_$(date +%Y%m%d)_$$.log"
        exit 1
    else
        echo_g "mvn install for ${project_clone_repository_name} successfully! "
    fi

    mvn clean package >>${WORKDIR}/mvn_build_$(date +%Y%m%d)_$$.log 2>&1
    retval=$?
    if [ ${retval} -ne 0 ] ; then
        echo_r "mvn clean package for ${project_clone_repository_name} failed! More details refer to ${WORKDIR}/mvn_build_$(date +%Y%m%d)_$$.log"
        exit 1
    else
        echo_g "mvn clean package for ${project_clone_repository_name} successfully! "
    fi
    cd ${WORKDIR}
    echo_g "Do mvn build java project finished for ${project_clone_repository_name} with exit code 0! "
    echo
}

# ssh_execute_command_on_remote_host hostname command
function ssh_execute_command_on_remote_host(){
    [ $# -ne 2 ] && return 1
    ssh -i /etc/ssh/ssh_host_rsa_key -p 22 -oStrictHostKeyChecking=no root@$1 "$2" >>${WORKDIR}/ssh_command_$(date +%Y%m%d)_$$.log 2>&1
    retval=$?
    if [ ${retval} -ne 0 ] ; then
        echo_r "ssh execute command on remote host $2 failed! "
        test -s ${WORKDIR}/ssh_command_$(date +%Y%m%d)_$$.log && echo_r "\tMore details refer to ${WORKDIR}/ssh_command_$(date +%Y%m%d)_$$.log"
        return 1
    else
        echo_g "ssh execute command on remote host $2 successfully! "
        return 0
    fi
}

function restart_docker_container(){
    echo_b "Restarting docker container..."
    [ $# -ne 2 ] && return 1
    # TODO(Guodong Ding) if we need restart more related docker container
    local user_defined_docker_container_name=""
    local remote_host_ip=""
    test -n $1 && remote_host_ip="$1"
    test -n $1 && user_defined_docker_container_name="$2"
    ssh_execute_command_on_remote_host "$remote_host_ip" "docker restart $user_defined_docker_container_name"
    retval=$?
    if [ ${retval} -ne 0 ] ; then
        echo_r "restart docker container for  $user_defined_docker_container_name on $remote_host_ip failed! "
        exit 1
    else
        echo_g "restart docker container for $user_defined_docker_container_name on $remote_host_ip successfully! "
        return 0
    fi
}

# scp_local_files_to_remote_host local_path remote_hostname remote_path
function scp_local_files_to_remote_host(){
    [ $# -ne 3 ] && return 1
    [ ! -d $1 -a ! -f $1 ] && return 1
#    check_ssh_can_be_connect $2
    scp -i /etc/ssh/ssh_host_rsa_key -P 22 -oStrictHostKeyChecking=no -rp $1 root@$2:$3 >/dev/null 2>&1
    retval=$?
    if [ ${retval} -ne 0 ] ; then
        echo_r "scp local files to remote host failed! "
        exit 1
    else
        echo_g "scp local files to remote host successfully! "
    fi

}

# scp_remote_files_to_local_host remote_hostname remote_path local_path
function scp_remote_files_to_local_host(){
    [ $# -ne 3 ] && return 1
#    check_ssh_can_be_connect $1
    scp -i /etc/ssh/ssh_host_rsa_key -P 22 -oStrictHostKeyChecking=no -rp root@$1:$2 $3 >/dev/null 2>&1
    retval=$?
    if [ ${retval} -ne 0 ] ; then
        echo_r "scp remote files to local host failed! "
        exit 1
    else
        echo_g "scp remote files to local host successfully! "
    fi
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
    test -f ${backup_filename_origin} && cp ${backup_filename_origin} ${backup_filename_target}
    set +o errexit
}


# Function description: backup files
# Note: accept $@ parameters
function backup_files(){
    # TODO(Guodong Ding) improvements here
    set -o errexit
    if [ $# -eq 0 ]; then
        return 1
    fi
    file_list=$@
    operation_date_time="_`date +"%Y%m%d%H%M%S"`"
    log_filename=".log_$$_${RANDOM}"
    log_filename_full_path=/tmp/${log_filename}
    touch ${log_filename_full_path}
    old_IFS=$IFS
    IFS=" "
    for file in ${file_list};do
        real_file=$(realpath ${file})
        [ -f ${real_file} ] && cp ${real_file} ${file}${operation_date_time}~
        [ -f ${log_filename_full_path} ] && echo "\mv -f $file$operation_date_time~ $file" >>${log_filename_full_path}
    done
    IFS="$old_IFS"
    set +o errexit
    return 0
}

# Function description:
function rollback_files(){
    # TODO(Guodong Ding) improvements here
    [ -f ${log_filename_full_path} ] && . ${log_filename_full_path}
    \rm -f ${log_filename_full_path}
    exit 2
}

function backup_directories(){
    # TODO(Guodong Ding) continue here
    if [ $# -ne 1 ]; then
        return 1
    fi
    backup_filename_origin="$1"
    operation_date_time="`date +"%Y%m%d%H%M%S"`"
    backup_filename_prefix=".backup_"
    backup_filename_suffix="_origin_$operation_date_time~"
    backup_filename_target="$backup_filename_prefix$backup_filename_origin$backup_filename_suffix"
    test -f ${backup_filename_origin} && cp -r ${backup_filename_origin} ${backup_filename_target}
}

function rollback_directories(){
    # TODO(Guodong Ding) continue here
    return
}


#
function backup_remote_host_config_files(){
    # TODO(Guodong Ding) did not throw a exception when first deploy and test -z "$user_defined_project_conf_directory"
    echo_b "backup remote host config files..."

    # backup operation only executed once time, using '$0 backup_manual' backup new configuration files.
    # if ${WORKDIR}/backup is not empty then return 0 to exit
    if [ "$(ls -A ${WORKDIR}/backup)" ]; then
        [ -f ${WORKDIR}/backup/.backup_operation_once.log ] && backup_operation="`cat ${WORKDIR}/backup/.backup_operation_once.log`"
        echo_g "Backup remote host config files operation had been done, $backup_operation, now skipping ... "
        return 0
    fi

    # TODO(Guodong Ding) if $user_defined_project_conf_directory is empty and remote host target directory is empty(first deploy), will cause exit with 1
    ssh_execute_command_on_remote_host ${user_defined_deploy_target_host_ip} "test \"\$(ls -A $user_defined_project_top_directory_to_target_host 2>/dev/null)\""
    if test $? -eq 0; then
        scp_remote_files_to_local_host ${user_defined_deploy_target_host_ip} ${user_defined_project_top_directory_to_target_host}/* ${WORKDIR}/backup
        # get config files
        [ "$(ls -A ${WORKDIR}/backup)" ] && find ${WORKDIR}/backup/. -type f ! -name . -a ! -name '*.xml*' -a ! -name '*.properties*' -a ! -name '*.version*' -exec rm -f -- '{}' \;
        # remove empty directory, 'for + rmdir'
        find ${WORKDIR}/backup/. -empty -type d -delete
        # TODO(Guodong Ding) improvements here
        echo_g "backup remote host config files finished."
        echo "`date +%Y%m%d`" > ${WORKDIR}/backup/.backup_operation_once.log
    else
        echo_y "This maybe first time to deploy or variable 'user_defined_project_conf_directory' is not defined! "
    fi
}

function rollback_remote_host_config_files(){
    echo_b "rollback remote host config files..."
    #scp_local_files_to_remote_host ${WORKDIR}/backup ${user_defined_deploy_target_host_ip} ${user_defined_project_top_directory_to_target_host}
    saved_IFS=$IFS
    IFS=' '
    cd ${WORKDIR}/current
    for file in ${WORKDIR}/backup/*;do
        scp_local_files_to_remote_host ${file} ${user_defined_deploy_target_host_ip} ${user_defined_project_top_directory_to_target_host}
        # override all configuration files to current
        \cp -r ${file} ${WORKDIR}/current
    done
    cd ${WORKDIR}
    IFS=${saved_IFS}
    # TODO(Guodong Ding) if save remote host config files, if there are no changes on config files
    # some ops

    # TODO(Guodong Ding) improvements here
    echo_g "rollback remote host config files finished."
}

function make_current_workable_source(){
    # check a directories lock, Note: this is redundant
    if [[ ! -f ${WORKDIR}/.capistrano_ds_lock ]]; then
        setDirectoryStructureOnLocalHost
    fi
    clean_old_releases
    clean_old_logs
    # do dependencies checking
    if test ! -z ${user_defined_skip_check_network_and_resolver}; then
        echo_g "skipping checking network connectivity and name resolve."
    else
        check_network_connectivity
        check_name_resolve
    fi

    check_other_dependencies

    # do core job
    # TODO(Guodong Ding) if we need a git_project_clone "$user_defined_project_clone_depends" here using auto judgment statement
    test -z ${user_defined_project_clone_depends} || git_project_clone "$user_defined_project_clone_depends"
    git_project_clone "$user_defined_project_clone"
    test -z ${user_defined_project_clone_depends} || maven_build_project "$user_defined_project_clone_depends"
    maven_build_project "$user_defined_project_clone"
    cd ${WORKDIR}

    # links_target_directory_to_current
    # Make directory to release directory
    if test ! -d ${WORKDIR}/release -o ! -d ${WORKDIR}/share; then
        echo_r "capistrano directory structure is broken, make sure the file .capistrano_ds_lock is deleted before a new deploy! "
#        test -f ${WORKDIR}/.capistrano_ds_lock && \rm -rf  ${WORKDIR}/.capistrano_ds_lock
        exit 1
    fi
    new_release_just_created="$WORKDIR/release/$(date +%Y%m%d%H%M%S)"
    [ ! -d ${new_release_just_created} ] && mkdir ${new_release_just_created}
    [ -d ${WORKDIR}/repository/${project_clone_repository_name}/target/${project_clone_repository_name}/ ] && \
        \cp -rf ${WORKDIR}/repository/${project_clone_repository_name}/target/${project_clone_repository_name}/* ${new_release_just_created}
     # Make source code symbolic link to current
    ( [ -f ${WORKDIR}/current ] || [ -d ${WORKDIR}/current ] ) && rm -rf ${WORKDIR}/current
    ln -s ${new_release_just_created} ${WORKDIR}/current

    # Move conf and logs directives from release to share if found
    [ -d ${WORKDIR}/release/conf ] && mv ${WORKDIR}/release/conf ${WORKDIR}/share/conf
    [ -d ${WORKDIR}/release/logs ] && mv ${WORKDIR}/release/logs ${WORKDIR}/share/logs

    # Make conf and logs symbolic link to current
    [ -d ${WORKDIR}/share/conf ] && ln -s ${WORKDIR}/share/conf ${WORKDIR}/current/conf
    [ -d ${WORKDIR}/share/logs ] && ln -s ${WORKDIR}/share/logs ${WORKDIR}/current/logs
}

# distribute current workable files to remote host
function deploy() {
    # do make_current_workable_source before deploy every time
    make_current_workable_source

    echo_b "Do deploy on $user_defined_deploy_target_host_ip ..."
    # backup remote host config files
    [ -z ${user_defined_project_conf_directory} ] && backup_remote_host_config_files

    saved_IFS=$IFS
    IFS=' '
    cd ${WORKDIR}/current
    for file in ${WORKDIR}/current/*;do
        scp_local_files_to_remote_host ${file} ${user_defined_deploy_target_host_ip} ${user_defined_project_top_directory_to_target_host}
    done
    cd ${WORKDIR}
    IFS=${saved_IFS}

    # rollback remote host config files
    [ -z ${user_defined_project_conf_directory} ] && rollback_remote_host_config_files
    if test ! -z "${user_defined_project_conf_directory}" -a -d ${user_defined_project_conf_directory} ; then
        saved_IFS=$IFS
        IFS=' '
        cd ${WORKDIR}/current
        for file in ${user_defined_project_conf_directory}/*;do
            scp_local_files_to_remote_host ${file} ${user_defined_deploy_target_host_ip} ${user_defined_project_top_directory_to_target_host}
            # override all configuration files to current
            \cp -rf ${file} ${WORKDIR}/current
        done
        cd ${WORKDIR}
        IFS=${saved_IFS}
    fi

    # backup remote host config files to local again for next using
    [ ! -z ${user_defined_project_conf_directory} ] && backup_remote_host_config_files

    # Start service or validate status on remote host
    if [[ -e ${WORKDIR}/current/bin/startup.sh ]]; then
        ssh_execute_command_on_remote_host ${user_defined_deploy_target_host_ip} "$user_defined_project_top_directory_to_target_host/bin/startup.sh start"
        RETVAL=$?
    else
        test -z ${user_defined_docker_container_name} || restart_docker_container ${user_defined_deploy_target_host_ip} ${user_defined_docker_container_name}
        # TODO(Guodong Ding) external health check
        RETVAL=$?
    fi

    # if started ok, then create a workable program to a file
    if [[ ${RETVAL} -eq 0 ]]; then
        # Note cat with eof must start at row 0, and with eof end only, such as no blank spaces, etc
        cat >${WORKDIR}/share/workable_program.log <<eof
${new_release_just_created}
eof
        echo_g "Deploy successfully for $user_defined_deploy_target_host_ip! "
        echo_g "Current workable version is $(cat ${WORKDIR}/share/workable_program.log)"
    else
        echo_r "Error: Deploy failed! "
        ${WORKDIR}/`basename $0` rollback
    fi
}

# Rollback to last right configuration
function rollback() {
    echo_b "Rollback to last right configuration... "
    # The key point is find last files which can work
    WORKABLE_PROGRAM=`cat ${WORKDIR}/share/workable_program.log`
    if [[ -z ${WORKABLE_PROGRAM} ]]; then
        echo_r "Error: Can NOT find workable release version! Please check if it is first deployment! "
        exit 1
    fi
    # Stop service if we have
    if [[ -e ${WORKDIR}/current/bin/startup.sh ]]; then
        ssh_execute_command_on_remote_host ${user_defined_deploy_target_host_ip} "$user_defined_project_top_directory_to_target_host/bin/startup.sh stop"
    fi

    # Remove failed deploy
    rm -rf ${WORKDIR}/current

    # Remake source code symbolic link to current
    ln -s ${WORKABLE_PROGRAM} ${WORKDIR}/current

    # Remake conf and logs symbolic link to current
    [ -d ${WORKDIR}/share/conf ] && ln -s ${WORKDIR}/share/conf ${WORKDIR}/current
    [ -d ${WORKDIR}/share/logs ] && ln -s ${WORKDIR}/share/logs ${WORKDIR}/current

    # backup remote host config files
    [ -z ${user_defined_project_conf_directory} ] && backup_remote_host_config_files

#    scp_local_files_to_remote_host ${WORKDIR}/current/ ${user_defined_deploy_target_host_ip} ${user_defined_project_top_directory_to_target_host}
    saved_IFS=$IFS
    IFS=' '
    cd ${WORKDIR}/current
    for file in ${WORKDIR}/current/*;do
        scp_local_files_to_remote_host ${file} ${user_defined_deploy_target_host_ip} ${user_defined_project_top_directory_to_target_host}
    done
    cd ${WORKDIR}
    IFS=${saved_IFS}

    # rollback remote host config files
    [ -z ${user_defined_project_conf_directory} ] && rollback_remote_host_config_files
    if test ! -z "${user_defined_project_conf_directory}" -a -d ${user_defined_project_conf_directory}; then
        saved_IFS=$IFS
        IFS=' '
        cd ${WORKDIR}/current
        for file in ${user_defined_project_conf_directory}/*;do
            scp_local_files_to_remote_host ${file} ${user_defined_deploy_target_host_ip} ${user_defined_project_top_directory_to_target_host}
        done
        cd ${WORKDIR}
        IFS=${saved_IFS}
    fi

    # Start service or validate status
    if [[ -e ${WORKDIR}/current/bin/startup.sh ]]; then
        ssh_execute_command_on_remote_host ${user_defined_deploy_target_host_ip} "$user_defined_project_top_directory_to_target_host/bin/startup.sh restart"
        RETVAL=$?
    else
        test -z ${user_defined_docker_container_name} || restart_docker_container ${user_defined_deploy_target_host_ip} ${user_defined_docker_container_name}
        # TODO(Guodong Ding) external health check
        RETVAL=$?
    fi

    # if started ok, then create a workable program to a file
    if [[ ${RETVAL} -eq 0 ]]; then
        echo_g "Rollback successfully! "
        echo_g "current workable version is $WORKABLE_PROGRAM"
    fi
}

# rollback to any workable version which user wished by manually
function rollback_manual(){
    echo_b "This function will rollback to any workable version which user wished by manually."
    # TODO(Guodong Ding) linux shell trap command several ctrl+c
    echo_p "Enter 'reset' command to reset terminal when something go wrong."
    read -e -s -n 1 -p "Press any key to continue or Press 'Ctrl+C' exit."
    if test -d ${WORKDIR}/release -a "$(ls -A ${WORKDIR}/release 2>/dev/null)" ;then # judge a directory if is empty
        echo_b "Current workable releases( Latest 5 ) are here: "
        # Alternative implementation: ls -u -1 -d ${WORKDIR}/release/* | tail -n6 | sed -n '1,4p'
        ls -u -1 -d ${WORKDIR}/release/* | tail -n6 | head -n4
        read -p "Which release do you want rollback? Press Enter after input. " user_input_release_to_rollback
        if test -d ${user_input_release_to_rollback}; then
            rm -rf ${WORKDIR}/current
            ln -s ${user_input_release_to_rollback} ${WORKDIR}/current
            # Remake conf and logs symbolic link to current
            [ -d ${WORKDIR}/share/conf ] && ln -s ${WORKDIR}/share/conf ${WORKDIR}/current
            [ -d ${WORKDIR}/share/logs ] && ln -s ${WORKDIR}/share/logs ${WORKDIR}/current

            # backup remote host config files
            [ -z ${user_defined_project_conf_directory} ] && backup_remote_host_config_files

#            # rollback remote host config files
#            [ -z ${user_defined_project_conf_directory} ] && rollback_remote_host_config_files

            if test ! -z "${user_defined_project_conf_directory}" -a -d ${user_defined_project_conf_directory}; then
                saved_IFS=$IFS
                IFS=' '
                cd ${WORKDIR}/current
                for file in ${user_defined_project_conf_directory}/*;do
                    \cp -rf ${file} ${WORKDIR}/current
                done
                cd ${WORKDIR}
                IFS=${saved_IFS}
            fi

            saved_IFS=$IFS
            IFS=' '
            cd ${WORKDIR}/current
            for file in ${WORKDIR}/current/*;do
                # TODO(Guodong Ding) scp timeout
                scp_local_files_to_remote_host ${file} ${user_defined_deploy_target_host_ip} ${user_defined_project_top_directory_to_target_host}
            done
            cd ${WORKDIR}
            IFS=${saved_IFS}

            # Start service or validate status
            if [[ -e ${WORKDIR}/current/bin/startup.sh ]]; then
#                ${WORKDIR}/current/bin/startup.sh restart
                ssh_execute_command_on_remote_host ${user_defined_deploy_target_host_ip} "$user_defined_project_top_directory_to_target_host/bin/startup.sh restart"
                RETVAL=$?
            else
                test -z ${user_defined_docker_container_name} || restart_docker_container ${user_defined_deploy_target_host_ip} ${user_defined_docker_container_name}
                # TODO(Guodong Ding) external health check
                RETVAL=$?
            fi

            # if started ok, then create a workable program to a file
            if [[ ${RETVAL} -eq 0 ]]; then
                echo_g "Rollback successfully! "
                echo_g "current workable version is $user_input_release_to_rollback"
                cat >${WORKDIR}/share/workable_program.log <<eof
${user_input_release_to_rollback}
eof
    fi
        else
            echo_r "The release you want to rollback is not present, Please  try again! "
        fi
    else
        echo_r "Error: Can NOT find workable release version! Please check if it is first deployment! "
        exit 1
    fi

}

# backup remote hosts config files only,
# use this function when you modify some config files on remote host
function backup_manual(){
    set -o errexit
    echo_b "backup remote host config files..."
    scp_remote_files_to_local_host ${user_defined_deploy_target_host_ip} "${user_defined_project_top_directory_to_target_host}/*" ${WORKDIR}/backup
    # get config files
    [ "$(ls -A ${WORKDIR}/backup)" ] && find ${WORKDIR}/backup/. -type f ! -name . -a ! -name '*.xml*' -a ! -name '*.properties*' -a ! -name '*.version*' -exec rm -f -- '{}' \;
    # remove empty directory, 'for + rmdir'
    find ${WORKDIR}/backup/. -empty -type d -delete
    # TODO(Guodong Ding) improvements here
    echo_g "backup remote host config files finished."
    echo "`date +%Y%m%d`" > ${WORKDIR}/backup/.backup_operation_once.log
    set +o errexit
}

# distribute current workable files to remote hosts
function deploys() {
    # do make_current_workable_source before deploy every time
    make_current_workable_source

    echo_b "Do deploy on $user_defined_deploy_targets_host_ip_list ..."
    for remote_host_ip in ${user_defined_deploy_targets_host_ip_list};do
        echo_b "Do deploy on $remote_host_ip ..."
        saved_IFS=$IFS
        IFS=' '
        cd ${WORKDIR}/current
        for file in ${WORKDIR}/current/*;do
            scp_local_files_to_remote_host ${file} ${remote_host_ip} ${user_defined_project_top_directory_to_target_host}
        done
        cd ${WORKDIR}
        IFS=${saved_IFS}

        # rollback remote host config files
        [ -z ${user_defined_project_conf_directory} ] && rollback_remote_host_config_files
        if test ! -z "${user_defined_project_conf_directory}" -a -d ${user_defined_project_conf_directory}; then
            saved_IFS=$IFS
            IFS=' '
            cd ${WORKDIR}/current
            for file in ${user_defined_project_conf_directory}/*;do
                scp_local_files_to_remote_host ${file} ${remote_host_ip} ${user_defined_project_top_directory_to_target_host}
            done
            cd ${WORKDIR}
            IFS=${saved_IFS}
        fi

        # Start service or validate status on remote host
        if [[ -e ${WORKDIR}/current/bin/startup.sh ]]; then
    #        ${WORKDIR}/current/bin/startup.sh start
            ssh_execute_command_on_remote_host ${remote_host_ip} "$user_defined_project_top_directory_to_target_host/bin/startup.sh start"
            RETVAL=$?
        else
            test -z ${user_defined_docker_container_name} || restart_docker_container ${remote_host_ip} ${user_defined_docker_container_name}
            # TODO(Guodong Ding) external health check
            RETVAL=$?
        fi
        if [[ ${RETVAL} -eq 0 ]]; then
            echo_g "Deploy successfully on $remote_host_ip! "
        else
            echo_r "Error: Deploy failed! on $remote_host_ip! "
            echo_p "Try modify $user_defined_deploy_target_host_ip and using standalone deployment mode"
            exit 1
        fi
    done

    # if started ok, then create a workable program to a file
    if [[ ${RETVAL} -eq 0 ]]; then
        # Note cat with eof must start at row 0, and with eof end only, such as no blank spaces, etc
    cat >${WORKDIR}/share/workable_program.log <<eof
${new_release_just_created}
eof
        echo_g "Deploy finished! on $user_defined_deploy_targets_host_ip_list "
        echo_g "current workable version is $(cat ${WORKDIR}/share/workable_program.log)"
    #    ls --color=auto -l ${WORKDIR}/current
    #    ls --color=auto -l ${WORKDIR}/current/
    else
        echo_r "Error: Deploy failed! "
        ${WORKDIR}/`basename $0` rollbacks
    fi
}

function rollbacks(){
    echo_b "This function will rollback to any workable version which user wished by manually."
    # TODO(Guodong Ding) linux shell trap command several ctrl+c
    echo_p "Enter 'reset' command to reset terminal when something go wrong."
    read -e -s -n 1 -p "Press any key to continue or Press 'Ctrl+C' exit. Enter 'reset' command to reset terminal when something go wrong."
    if test -d ${WORKDIR}/release -a "$(ls -A ${WORKDIR}/release 2>/dev/null)" ;then # judge a directory if is empty
        echo_b "Current workable releases( Latest 5 ) are here: "
#        ls -d -1 ${WORKDIR}/release/*
        ls -u -1 -d ${WORKDIR}/release/* | tail -n5
        read -p "Which release do you want rollback? Press Enter after input. " user_input_release_to_rollback
        if test -d ${user_input_release_to_rollback}; then
            rm -rf ${WORKDIR}/current
            ln -s ${user_input_release_to_rollback} ${WORKDIR}/current
            # Remake conf and logs symbolic link to current
            [ -d ${WORKDIR}/share/conf ] && ln -s ${WORKDIR}/share/conf ${WORKDIR}/current
            [ -d ${WORKDIR}/share/logs ] && ln -s ${WORKDIR}/share/logs ${WORKDIR}/current

            # backup remote host config files
            [ -z ${user_defined_project_conf_directory} ] && backup_remote_host_config_files

            #    scp_local_files_to_remote_host ${WORKDIR}/current/ ${user_defined_deploy_target_host_ip} ${user_defined_project_top_directory_to_target_host}
            saved_IFS=$IFS
            IFS=' '
            cd ${WORKDIR}/current
            for host_ip in ${user_defined_deploy_targets_host_ip_list};do
                    for file in ${WORKDIR}/current/*;do
                        scp_local_files_to_remote_host ${file} ${user_defined_deploy_target_host_ip} ${user_defined_project_top_directory_to_target_host}
                    done
            done
            cd ${WORKDIR}
            IFS=${saved_IFS}

            # Start service or validate status
            if [[ -e ${WORKDIR}/current/bin/startup.sh ]]; then
#                ${WORKDIR}/current/bin/startup.sh restart
                ssh_execute_command_on_remote_host ${user_defined_deploy_target_host_ip} "$user_defined_project_top_directory_to_target_host/bin/startup.sh restart"
                RETVAL=$?
            else
                test -z ${user_defined_docker_container_name} || restart_docker_container ${user_defined_docker_container_name}
                # TODO(Guodong Ding) external health check
                RETVAL=$?
            fi

            # if started ok, then create a workable program to a file
            if [[ ${RETVAL} -eq 0 ]]; then
                echo_g "Rollback successfully on $user_defined_deploy_targets_host_ip_list! "
                echo_g "Current workable version is $user_input_release_to_rollback"
                cat >${WORKDIR}/share/workable_program.log <<eof
${user_input_release_to_rollback}
eof
    fi
        else
            echo_r "The release you want to rollback is not present, Please  try again! "
        fi
    else
        echo_r "Error: Can NOT find workable release version! Please check if it is first deployment! "
        exit 1
    fi

}

function destroy() {
    # echo a Warning message
    echo_y "Warning: This action will destroy all this project, and this is unrecoverable! "
    user_input_answer_want_do_destroy="n"
    echo_y "Do you want to destroy this project? "
    read -p "(Default no,if you want please input: y ,if not please press the enter button):" user_input_answer_want_do_destroy
    case "$user_input_answer_want_do_destroy" in
        y|Y|Yes|YES|yes|yES|yEs|YeS|yeS )
        # delete all file expect for this script self
        # find: warning: Unix filenames usually don't contain slashes (though pathnames do).  That means that '-name `./deploy.sh'' will probably evaluate to false all the time on this system.  You might find the '-wholename' test more useful, or perhaps '-samefile'.  Alternatively, if you are using GNU grep, you could use 'find ... -print0 | grep -FzZ `./deploy.sh''.
            # echo $WORKDIR/
            #find -L $WORKDIR -type f ! -name "$(basename $0)" -exec ls --color=auto -al {} \;
            # find -L . -type f ! -name "deploy.sh" -exec ls --color=auto -al {} \;
            # find -L . -type d -exec ls --color=auto -al {} \;
            # find -L ./ -maxdepth 1 ! -name "deploy.sh" ! -wholename "./"
        # ls | grep -v "filename" | xargs rm -rf
        find -L ${WORKDIR} -maxdepth 1 ! -name "$(basename $0)" ! -wholename "$WORKDIR"  -exec rm -rf '{}' \;
        if [ $? -eq 0 ];then
            test -f ${WORKDIR}/.capistrano_ds_lock && \rm -rf  ${WORKDIR}/.capistrano_ds_lock
            echo_g "Destroy this project successfully! Now will exit with status 0. "
            exit 0
        else
            echo_r "Error: something go wrong! Please check or alter to Admin user! "
            exit 1
        fi
        ;;
        n|N|No|NO|no|nO)
        echo_g "destroy action is cancel"
        exit 0
        ;;
        *)
        echo_r "Are you kidding me? You are a bad kid! "
        exit 1
        ;;
    esac

}

function usage(){
    cat - << eof
"${WORKDIR}/`basename $0` deploy              new deploy/ update one remote target host
"${WORKDIR}/`basename $0` rollback_manual     rollback to any workable version to one remote target host by manual
"${WORKDIR}/`basename $0` deploys             new deploy/ update more then one remote target host
"${WORKDIR}/`basename $0` rollbacks           rollback to any workable version to more than one remote target host by manual
"${WORKDIR}/`basename $0` backup_manual       backup conf files to local by manual when you add/delete/update conf files on remote target host
eof

}

function main(){
    lock_filename="lock_$$_${RANDOM}"
#    lock_filename_full_path="/var/lock/subsys/$lock_filename"
    lock_filename_full_path="/var/lock/$lock_filename"
    if ( set -o noclobber; echo "$$" > "$lock_filename_full_path") 2> /dev/null;then
        trap 'rm -f "$lock_filename_full_path"; exit $?' INT TERM EXIT
        [ ! -x ${WORKDIR}/`basename $0` ] && chmod +x ${WORKDIR}/`basename $0`
        [ -n "$header" ] && echo "$header"

        # if exist file '.capistrano_ds_lock', then this is not first deployment, and unset
        if test -f ${WORKDIR}/.capistrano_ds_lock; then
            unset user_defined_project_conf_directory
            user_defined_project_conf_directory=""
        fi

        if [[ $# -ne 1 ]]; then
            ${WORKDIR}/`basename $0` help
            exit 0
        fi
        case $1 in
            deploy)
                deployment_mode="1"
                deploy
                ;;
            rollback)
                rollback
                ;;
            rollback_manual|rollbackup_manual)
                rollback_manual
                ;;
            backup_manual)
                backup_manual
                ;;
            deploys)
                deployment_mode="0"
                deploys;
                ;;
            rollbacks|rollbackups)
                rollbacks
                ;;
            destroy)
                destroy
                ;;
            help|*)
                echo "Usage: $0 {deploy|rollback_manual|deploys|backup_manual} with $0 itself"
                usage
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
if ${DEBUG} ; then
    export PS4=${old_PS4}
    ${_XTRACE_FUNCTIONS}
fi

