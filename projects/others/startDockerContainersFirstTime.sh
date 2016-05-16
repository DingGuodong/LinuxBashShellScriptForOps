#!/bin/bash

# Name: startDockerContainersFirstTime.sh
# Execute this shell script to start Docker containers first time, usefull for system normal or exception to shut down or outage

# debug option
#_XTRACE_FUNCTIONS=$(set +o | grep xtrace)
#set -o xtrace

# define user friendly messages
header="
Execute this shell script to start Docker containers first time, usefull for system normal or exception to shut down or outage.
"

# define variables
# end define variables

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
    # Color blue: Debug, friendly prompt
    [ $# -ne 1 ] && return 1
    echo -e "\033[34m$1\033[0m"
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

function startDockerService(){
    test -x /etc/init.d/docker && service docker start || /etc/init.d/docker start
    if $? -ne 0 ; then
        test ! -f /var/log/docker -o ! -f /var/log/docker.log echo_b "docker daemon"
}

function checkDockerServiceStatus(){
    docker_pid="`ps -ef | grep '[d]ocker daemon' | awk '{print $2}'`"
    if test -z ${docker_pid} ; then
        echo_g "Docker engine service is running, process $docker_pid"
    else
        echo_r "Docker engine service is outage, try start it if we can"
        startDockerService
    fi
}

function startDockerContainersFirstTime(){
    return
}

function main(){
    lock_filename="lock_$$_$RANDOM"
#    lock_filename_full_path="/var/lock/subsys/$lock_filename"
    lock_filename_full_path="/var/lock/$lock_filename"
    if ( set -o noclobber; echo "$$" > "$lock_filename_full_path") 2> /dev/null;then
        trap 'rm -f "$lock_filename_full_path"; exit $?' INT TERM EXIT
        # Just a test for call itself, comment it
         if [[ $# -ne 1 ]]; then
#            $0 deploy
            [ ! -x ${WORKDIR}/`basename $0` ] && chmod +x ${WORKDIR}/`basename $0`
            ${WORKDIR}/`basename $0` deploy
            exit 0
         fi
        case $1 in
            deploy)
                deploy
                ;;
            rollback)
                rollback
                ;;
            destroy)
                destroy
                ;;
            help|*)
                echo "Usage: $0 {deploy|rollback|destroy} with $0 itself"
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

