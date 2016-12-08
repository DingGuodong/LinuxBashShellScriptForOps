#!/bin/bash
# bash shell template

# debug option
DEBUG=false

if ${DEBUG} ; then
    old_PS4=$PS4
#    export PS4='+${BASH_SOURCE}:${LINENO}:${FUNCNAME[0]}: '
    export PS4='+${LINENO}: ${FUNCNAME[0]}: ' # if there is only one bash script, do not display ${BASH_SOURCE}
    _XTRACE_FUNCTIONS=$(set +o | grep xtrace)
    set -o xtrace
fi

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

function usage(){
    cat - <<eof
For reference only, this is just a demo.
using this script to find files in a specified directory
    between 'time_start' to 'time_end', or find files between 'time_start' to now.
default directory is "/tmp/.test", and this is fixed, please change it to changeable or other names which you need.
function generate_test_example(), juet a sample test, it is called in function main(), remove it as you wish.
eof

    cat - <<eof
Example:
# ls /tmp/.test/ -al
total 8
drwxr-xr-x 2 root root 4096 Dec  8 12:36 .
drwxrwxrwt 3 root root 4096 Dec  8 12:35 ..
-rw-r--r-- 1 root root    0 Dec  8 12:35 global2.log.20161208.123505
-rw-r--r-- 1 root root    0 Dec  8 12:35 global2.log.20161208.123507
-rw-r--r-- 1 root root    0 Dec  8 12:35 global2.log.20161208.123508
-rw-r--r-- 1 root root    0 Dec  8 12:35 global2.log.20161208.123524
-rw-r--r-- 1 root root    0 Dec  8 12:35 global2.log.20161208.123527
-rw-r--r-- 1 root root    0 Dec  8 12:35 global2.log.20161208.123535
-rw-r--r-- 1 root root    0 Dec  8 12:35 global2.log.20161208.123543
-rw-r--r-- 1 root root    0 Dec  8 12:35 global2.log.20161208.123547
-rw-r--r-- 1 root root    0 Dec  8 12:35 global2.log.20161208.123551
-rw-r--r-- 1 root root    0 Dec  8 12:35 global2.log.20161208.123559
-rw-r--r-- 1 root root    0 Dec  8 12:36 global2.log.20161208.123607
# ./tt.sh 20161208.123550
-rw-r--r-- 1 root root 0 Dec  8 12:35 /tmp/.test/global2.log.20161208.123551
-rw-r--r-- 1 root root 0 Dec  8 12:35 /tmp/.test/global2.log.20161208.123559
-rw-r--r-- 1 root root 0 Dec  8 12:36 /tmp/.test/global2.log.20161208.123607
# ./tt.sh 20161208.123550 20161208.123559
-rw-r--r-- 1 root root 0 Dec  8 12:35 /tmp/.test/global2.log.20161208.123551
#
eof

}

function date_format_transform(){
    # date --date='2016-12-08 12:49:56' +"%Y%m%d.%H%M%S"
    # python -c "import time;print time.mktime(time.strptime('20160823.140801', '%Y%m%d.%H%M%S'))"
    if [ "x$1" != "x" ]; then
        unix_timestamp=$(python -c "import time;print time.mktime(time.strptime('$1', '%Y%m%d.%H%M%S'))")
        result=$(date -d@"$unix_timestamp" +"%Y-%m-%d %H:%M:%S")
        echo "${result}"
    else
        echo "bad parameter"
        exit
    fi
}

function find_with_time_from_range(){
    # find /tmp/.test/ -type f -newermt '2016-12-08 12:35:07' ! -newermt '2016-12-08 12:35:51'
    if test "x$1" != "x" -a "x$2" != "x" ; then
        time_start=$(date_format_transform $1)
        time_end=$(date_format_transform $2)
        find /tmp/.test/ -type f -newermt "${time_start}" ! -newermt "${time_end}" | xargs ls -al
    else
        exit
    fi

}

function find_with_time_to_now(){
    # find /tmp/.test/ -type f -newermt '2016-12-08 12:35:07'
    if test "x$1" != "x" -a "x$2" == "x" ; then
        time_start=$(date_format_transform $1)
        find /tmp/.test/ -type f -newermt "${time_start}" | xargs ls -al
    else
        exit
    fi

}

function generate_test_example() {
    echo "generating test example directories and files... Please waiting 0~max(10*9) seconds."
    date_format="%Y%m%d.%H%M%S"
    # filename_tail="`date +"$date_format"`"
    [ -d /tmp/.test ] || mkdir -p /tmp/.test
    for (( i=1 ; i<10 ; i++ )); do
        touch /tmp/.test/global2.log."`date +"$date_format"`"
        sleep "`expr $RANDOM % 9`"
    done
    [ -d /tmp/.test ] && ls -al /tmp/.test
}

function main(){
    lock_filename="lock_$$_$RANDOM"
#    lock_filename_full_path="/var/lock/subsys/$lock_filename"
    lock_filename_full_path="/var/lock/$lock_filename"
    if ( set -o noclobber; echo "$$" > "$lock_filename_full_path") 2> /dev/null;then
        trap 'rm -f "$lock_filename_full_path"; exit $?' INT TERM EXIT
        # do something here
        generate_test_example
        if [[ "x$@" == "x" ]]; then
            usage
        else
            if test "x$1" != "x" -a "x$2" != "x" ; then
                find_with_time_from_range $@
            elif test "x$1" != "x" -a "x$2" == "x" ; then
                find_with_time_to_now $@
            else
                usage
            fi
        fi
        # end do something here
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
