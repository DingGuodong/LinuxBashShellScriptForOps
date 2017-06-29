#!/usr/bin/env bash
# a command or alias to replace 'rm' with a safe and easy to use, safe remove files or directories
# See also: safe-rm - wrapper around the rm command to prevent accidental deletions


# debug option
DEBUG=false  # DEBUG=true

if ${DEBUG} ; then
    old_PS4=$PS4
#    export PS4='+${BASH_SOURCE}:${LINENO}:${FUNCNAME[0]}: '
    export PS4='+${LINENO}: ${FUNCNAME[0]}: ' # if there is only one bash script, do not display ${BASH_SOURCE}
    _XTRACE_FUNCTIONS=$(set +o | grep xtrace)
    set -o xtrace
fi

# set an empty function using for location this line quickly in PyCharm editor on purpose.
function _empty() { return; }


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


real_rm='/bin/rm'
trash_dir="$HOME/.trash"  # if do not use "$HOME" or "~" to resolve permission problem, should use "chmod o+t $trash_dir" .chmod --help: Each MODE is of the form `[ugoa]*([-+=]([rwxXst]*|[ugo]))+'.
log_dir="$trash_dir"
trash_save_days=3

function real_rm() {

    if [[ ! -f ${real_rm} ]]; then
        echo 'safe-rm cannot find the real "rm" binary'
        exit 1
    fi

    save_days=${trash_save_days:-10}

    test $(find -L /tmp/.delete/ -type d ! -name "^." -a ! -wholename "/tmp/.delete/"  -mtime +${save_days} -exec echo '{}' \; | wc -l ) -gt 0
    found_old_files=$?
    if [[ ${found_old_files} -eq 0 ]]; then
        echo_b "old files found, cleaning"
        #find -L ${trash_dir}/ -maxdepth 1 -type d ! -name "^." -mtime +${save_days} -exec rm -rf '{}' \;
        find -L ${trash_dir}/ -maxdepth 1 -type d ! -wholename "$trash_dir/" ! -name "^." -mtime +${save_days} -exec rm -rf '{}' \;
        echo_g "old files cleaned successfully"
    else
        echo_g "old files in standby state, passed"
    fi
}

function safe_rm() {
    if [[ "$1x" = 'x' ]]; then
        ${real_rm} --help
        exit 1
    fi

    if [[ ! -d ${trash_dir} ]]; then
        mkdir -p ${trash_dir}
    fi

    # date +%Y%m%d%H%M%S.%N | shasum | awk '{print $1}' | cat - -A
    uniq_trash_dir="$trash_dir/$(date +%Y%m%d%H%M%S.%N | shasum | awk '{print $1}')"
    mkdir -p ${uniq_trash_dir}

    if [[ $# -eq 1 ]];then
        if [[ -f $1 ]] || [[ -d $1 ]]; then  # ignore rm -f|-r|-rf|-fr, etc
            mv $1 ${uniq_trash_dir}
            retval=$?
        fi
    else
        # alternative impl of 'rm FILE...'
        parameter_array="$@"
        # IFS=' '$'\t'$'\n', IFS=$' \t\n', If IFS is unset, or its value is exactly <space><tab><newline>
        old_IFS=$IFS
        IFS=' '$'\t'$'\n'
        for parameter in ${parameter_array}; do
            if [[ -f ${parameter} ]] || [[ -d ${parameter} ]]; then  # ignore rm -f|-r|-rf|-fr, etc
                mv ${parameter} ${uniq_trash_dir}
            fi
        done
        retval=$?
        IFS="$old_IFS"
    fi

    log_operation $@
    exit ${retval}
}

function log_operation(){
    tee -a ${log_dir}/operation.log <<-eof  # debug purpose or notify mode
{
    "date_human": "$(date +'%Y-%m-%d %H:%M:%S.%N')",
    "date": "$(date)",
    "user": "$USER",
    "ssh_client": "$SSH_CLIENT",
    "ssh_connection": "$SSH_CONNECTION",
    "ssh_tty": "$SSH_TTY",
    "trash_dir": "$uniq_trash_dir"
    "pwd": "$PWD",
    "operation": "$0 $@",
    "parameter": "$@"

}
eof
}


function usage(){
    cat - << eof
${WORKDIR}/`basename $0` help       show help message
${WORKDIR}/`basename $0` clean      clean old deleted files
eof

}


function main(){
    lock_filename="lock_$$_${RANDOM}"
#    lock_filename_full_path="/var/lock/subsys/$lock_filename"
    lock_filename_full_path="/var/lock/$lock_filename"
    if ( set -o noclobber; echo "$$" > "$lock_filename_full_path") 2> /dev/null;then
        trap 'rm -f "$lock_filename_full_path"; exit $?' INT TERM EXIT
        [ ! -x ${WORKDIR}/`basename $0` ] && chmod +x ${WORKDIR}/`basename $0`

        if [[ $# -lt 1 ]]; then
            ${WORKDIR}/`basename $0` help
            exit 0
        fi

        if [ -f $1 ]; then
            safe_rm $@
        else
            parameter_array="$@"
            # IFS=' '$'\t'$'\n', IFS=$' \t\n', If IFS is unset, or its value is exactly <space><tab><newline>
            old_IFS=$IFS
            IFS=' '$'\t'$'\n'
            for parameter in ${parameter_array}; do
                if [[ -f ${parameter} ]] || [[ -d ${parameter} ]]; then  # ignore rm -f|-r|-rf|-fr, etc
                    safe_rm $@
                fi
            done
            IFS="$old_IFS"
        fi

        case $1 in
            clean)
                real_rm
                ;;
            help|*)
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

