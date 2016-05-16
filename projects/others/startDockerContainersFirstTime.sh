#!/bin/bash

# Name: startDockerContainersFirstTime.sh
# Execute this shell script to start Docker containers first time, useful for system normal or exception to shut down or outage
# Do NOT modify anything expect for "user defined variables" unless you know what it means and what are you doing.

# debug option
#_XTRACE_FUNCTIONS=$(set +o | grep xtrace)
#set -o xtrace

# define user friendly messages
header="
Execute this shell script to start Docker containers first time, useful for system normal or exception to shut down or outage.
"

# user defined variables
docker_interconnection_network_name=""
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
    echo "WARNING: Running as a non-root user, \"$LOGNAME\". Functionality may be unavailable. Only root can use some commands or options"
fi

function startDockerService(){
    docker_pid="`ps -ef | grep '[d]ocker daemon' | awk '{print $2}'`"
    if test -z ${docker_pid} ; then
        test -x /etc/init.d/docker && service docker start || /etc/init.d/docker start
        if test $? -ne 0 ; then
            if test ! -f /var/log/docker; then
                echo_r "Error: Docker engine service start failed! "
                echo_b "try to use \"docker daemon\" see what failure occurs during start Docker engine service."
                docker daemon
            else
                echo_r "Error: Docker engine service start failed! "
                echo_b "see file \"/var/log/docker\" for more details"
            fi
        else
            docker_pid="`ps -ef | grep '[d]ocker daemon' | awk '{print $2}'`"
            echo_g "Docker engine service is running, process $docker_pid"
        fi
    else
        echo_g "Docker engine service is already running, process $docker_pid."
    fi
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

function checkDockerNetworkStatus(){
    test -z ${docker_interconnection_network_name} || docker_interconnection_network_name="docker_connection"
    docker network inspect ${docker_interconnection_network_name} >/dev/null 2>&1
    if test $? -ne 0 ; then
        docker network create ${docker_interconnection_network_name}
        checkDockerNetworkStatus
    else
        echo_g "Docker network check passed! "
    fi
}

function startDockerContainersMemcached(){
    docker run --restart="always" -d -v /etc/localtime:/etc/localtime --name memcached-os-static memcached
    docker run --restart="always" -d -v /etc/localtime:/etc/localtime --name memcached-os-dynamic memcached memcached -m 128
    docker run --restart="always" -d -v /etc/localtime:/etc/localtime --name memcached-bs-static memcached
    docker run --restart="always" -d -v /etc/localtime:/etc/localtime --name memcached-bs-dynamic memcached memcached -m 128
    docker run --restart="always" -d -v /etc/localtime:/etc/localtime --name memcached-activity memcached memcached -m 128
    docker run --restart="always" -d -v /etc/localtime:/etc/localtime --name memcached-envelope memcached memcached

    docker network connect docker_connection memcached-os-static
    docker network connect docker_connection memcached-os-dynamic
    docker network connect docker_connection memcached-bs-static
    docker network connect docker_connection memcached-bs-dynamic
    docker network connect docker_connection memcached-activity
    docker network connect docker_connection memcached-envelope
}

function startDockerContainersActiveMQ(){
    docker run --restart="always" -d --name amq-server \
        -e 'ACTIVEMQ_MIN_MEMORY=512' \
        -e 'ACTIVEMQ_MAX_MEMORY=2048' \
        -e 'ACTIVEMQ_NAME=amqp-srv1' \
        -e 'ACTIVEMQ_ADMIN_LOGIN=huntor' \
        -e 'ACTIVEMQ_ADMIN_PASSWORD=ht_2015' \
        -e 'ACTIVEMQ_ENABLED_SCHEDULER=true' \
        -v /data/docker/amq-server/data:/data/activemq \
        -v /data/docker/amq-server/logs:/var/log/activemq \
        -v /etc/localtime:/etc/localtime \
        -p 10201:8161 \
        -p 10202:61616 \
        -p 10203:61613 \
        webcenter/activemq

    docker network connect docker_connection amq-server
}

function startDockerContainersRedis(){
    docker run -d --restart="always" --name redis-os \
        -v /data/docker/redis-os/data:/data \
        -v /etc/localtime:/etc/localtime \
        -p 10302:6379 redis redis-server --appendonly yes

    docker run -d --restart="always" --name redis-bs \
        -v /data/docker/redis-bs/data:/data \
        -v /etc/localtime:/etc/localtime \
        -p 10301:6379 redis redis-server --appendonly yes

    docker network connect docker_connection redis-os
    docker network connect docker_connection redis-bs

}

function startDockerContainersEnvelope(){
    docker run -dit --restart="always" -p 10059:8080 --name "envelope-01" \
        -v /data/docker/envelope-01:/data/tomcat-8.0.21/webapps/Envelope \
        -v /data/docker/logs/envelope-01:/data/tomcat-8.0.21/logs \
        -v /etc/localtime:/etc/localtime \
        docker.huntor.cn/jdk8-tomcat8

    docker network connect docker_connection envelope-01

}

function startDockerContainersOS(){
    #os-gateway
    docker run -dit --restart="always" -p 10401:8080 -p 10402:8000 --name "os-gw-01" \
        -v /data/docker/opensocial/os-gw-01:/data/tomcat-8.0.21/webapps/opensocial-gateway \
        -v /data/docker/logs/os-gw-01:/data/tomcat-8.0.21/logs \
        -v /etc/localtime:/etc/localtime \
        docker.huntor.cn/jdk8-tomcat8

    docker network connect docker_connection os-gw-01

    #os-msg
    docker run -dit --restart="always" -p 10403:8080 -p 10404:8000 --name "os-msg-01" \
        -v /data/docker/opensocial/os-msg-01:/data/tomcat-8.0.21/webapps/opensocial-message \
        -v /data/docker/logs/os-msg-01:/data/tomcat-8.0.21/logs \
        -v /etc/localtime:/etc/localtime \
        docker.huntor.cn/jdk8-tomcat8

    docker network connect docker_connection os-msg-01

    #os-inte
    docker run -dit --restart="always" -p 10405:8080 -p 10406:8000 --name "os-inte-01" \
        -v /data/docker/opensocial/os-inte-01:/data/tomcat-8.0.21/webapps/opensocial-integration \
        -v /data/docker/logs/os-inte-01:/data/tomcat-8.0.21/logs \
        -v /etc/localtime:/etc/localtime \
        docker.huntor.cn/jdk8-tomcat8

    docker network connect docker_connection os-inte-01

    #os-dsp
    docker run -dit --restart="always" -p 10407:8080 -p 10408:8000 --name "os-dsp-01" \
        -v /data/docker/opensocial/os-dsp-01:/data/tomcat-8.0.21/webapps/opensocial-dsp \
        -v /data/docker/logs/os-dsp-01:/data/tomcat-8.0.21/logs \
        -v /etc/localtime:/etc/localtime \
        docker.huntor.cn/jdk8-tomcat8

    docker network connect docker_connection os-dsp-01

    #os-web
    docker run -dit --restart="always" -p 10409:8080 -p 10410:8000 --name "os-web-01" \
        -v /data/docker/opensocial/os-web-01:/data/tomcat-8.0.21/webapps/opensocial-wechat-web \
        -v /data/docker/logs/os-web-01:/data/tomcat-8.0.21/logs \
        -v /etc/localtime:/etc/localtime \
        docker.huntor.cn/jdk8-tomcat8

    docker network connect docker_connection os-web-01

}

function startDockerContainersBS(){
#    bs-core
    docker run -dit --restart="always" -p 10501:8080 -p 10502:8000 --name "bs-core-01" \
        -v /data/docker/business-service/bs-core-01:/data/tomcat-8.0.21/webapps/business-service-core \
        -v /data/docker/logs/bs-core-01:/data/tomcat-8.0.21/logs \
        -v /etc/localtime:/etc/localtime \
        docker.huntor.cn/jdk8-tomcat8

    docker network connect docker_connection bs-core-01

#    bs-mobile
    docker run -dit --restart="always" -p 10503:8080 -p 10504:8000 --name "bs-mobile-01" \
        -v /data/docker/business-service/bs-mobile-01:/data/tomcat-8.0.21/webapps/business-service-mobile \
        -v /data/docker/logs/bs-mobile-01:/data/tomcat-8.0.21/logs \
        -v /etc/localtime:/etc/localtime \
        docker.huntor.cn/jdk8-tomcat8

    docker network connect docker_connection bs-mobile-01

#    bs-dsp
    docker run -dit --restart="always" -p 10505:8080 -p 10506:8000 --name "bs-dsp-01" \
        -v /data/docker/business-service/bs-dsp-01:/data/tomcat-8.0.21/webapps/business-service-dsp \
        -v /data/docker/logs/bs-dsp-01:/data/tomcat-8.0.21/logs \
        -v /etc/localtime:/etc/localtime \
        docker.huntor.cn/jdk8-tomcat8

    docker network connect docker_connection bs-dsp-01

#    bs-message
    docker run -dit --restart="always" -p 10507:8080 -p 10508:8000 --name "bs-message-01" \
        -v /data/docker/business-service/bs-message-01:/data/tomcat-8.0.21/webapps/business-service-message \
        -v /data/docker/logs/bs-message-01:/data/tomcat-8.0.21/logs \
        -v /etc/localtime:/etc/localtime \
        docker.huntor.cn/jdk8-tomcat8

    docker network connect docker_connection bs-message-01

#    bs-chatter
    docker run -dit --restart="always" -p 10509:29092 -p 10510:8000 --name "bs-chatter-01" \
        -v /data/docker/business-service/bs-chatter-01:/data/chatter \
        -v /data/docker/logs/bs-chatter-01:/data/chatter/logs \
        -v /etc/localtime:/etc/localtime \
        docker.huntor.cn/jdk8-chatter

    docker network connect docker_connection bs-chatter-01

#    bs-publish
    docker run -dit --restart="always" -p 10513:8080 -p 10514:8000 --name "bs-publish-01" \
    -v /data/docker/business-service/bs-publish-01:/data/tomcat-8.0.21/webapps/business-service-publish \
    -v /data/docker/logs/bs-publish-01:/data/tomcat-8.0.21/logs \
    -v /etc/localtime:/etc/localtime \
    docker.huntor.cn/jdk8-tomcat8

    docker network connect docker_connection bs-publish-01

#    bs-serviceorder
    docker run -dit --restart="always" -p 10517:8080 -p 10518:8000 --name "bs-serviceorder-01" \
        -v /data/docker/business-service/bs-serviceorder-01:/data/tomcat-8.0.21/webapps/business-service-serviceorder \
        -v /data/docker/logs/bs-serviceorder-01:/data/tomcat-8.0.21/logs \
        -v /etc/localtime:/etc/localtime \
        docker.huntor.cn/jdk8-tomcat8

    docker network connect docker_connection bs-serviceorder-01
}

function start(){
    checkDockerServiceStatus
    checkDockerNetworkStatus
    set -o errexit
    startDockerContainersMemcached
    startDockerContainersActiveMQ
    startDockerContainersRedis
    startDockerContainersEnvelope
    startDockerContainersOS
    startDockerContainersBS
    set +o errexit
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
            ${WORKDIR}/`basename $0` start
            exit 0
         fi
        case $1 in
            start)
                start
                ;;
            help|*)
                echo "Usage: $0 {start} with $0 itself"
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

