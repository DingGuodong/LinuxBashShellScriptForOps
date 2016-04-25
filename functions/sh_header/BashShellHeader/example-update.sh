#!/usr/bin/env bash

# Public header
# =============================================================================================================================

# Check that we are root ... so non-root users stop here
[  `id -u` -eq  "0" ] ||  exit 4

# resolve links - $0 may be a symbolic link
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


# echo color function
function cecho {
    # Usage:
    # cecho -red sometext     #Error, Failed
    # cecho -green sometext   # Success
    # cecho -yellow sometext  # Warning
    # cecho -blue sometext    # Debug
    # cecho -white sometext   # info
    # cecho -n                # new line
    # end

    while [ "$1" ]; do
        case "$1" in
            -normal)        color="\033[00m" ;;
# -black)         color="\033[30;01m" ;;
-red)           color="\033[31;01m" ;;
-green)         color="\033[32;01m" ;;
-yellow)        color="\033[33;01m" ;;
-blue)          color="\033[34;01m" ;;
# -magenta)       color="\033[35;01m" ;;
# -cyan)          color="\033[36;01m" ;;
-white)         color="\033[37;01m" ;;
-n)             one_line=1;   shift ; continue ;;
*)              echo -n "$1"; shift ; continue ;;
esac

shift
echo -en "$color"
echo -en "$1"
echo -en "\033[00m"
shift

done
if [ ! $one_line ]; then
        echo
fi
}
# end echo color function

# echo color function, smarter
function echo_r () {
    #Error, Failed
    [ $# -ne 1 ] && return 0
    echo -e "\033[31m$1\033[0m"
}
function echo_g () {
    # Success
    [ $# -ne 1 ] && return 0
    echo -e "\033[32m$1\033[0m"
}
function echo_y () {
    # Warning
    [ $# -ne 1 ] && return 0
    echo -e "\033[33m$1\033[0m"
}
function echo_b () {\
    # Debug
    [ $# -ne 1 ] && return 0
    echo -e "\033[34m$1\033[0m"
}
# end echo color function, smarter

WORKDIR=$PRGDIR
# end public header
# =============================================================================================================================

# begin customization for special case
# =============================================================================
# project directory to waiting for update
config_project_dir=example_projects
# resources directory which contains config file and update files
config_resources_dir=example_resources
# backup directory which to contains backup of whole project
config_backup_dir=example_backup_dir
# remote options, "y" can be supported, "-" not supported
    #config_remote_execution=yes|no             [y]
    #config_remote_execution=true|false         [y]
    #config_remote_execution=enable|disable     [-], conflicted to bash
    #config_remote_execution=1|0                [y]
config_remote_execution=no
# TODO
# not ready for remote execution
# if config_remote_execution set to true, then blew is a must
config_remote_backup_server=
config_remote_backup_directory=
# end customization for special case
# =============================================================================

# this is can NOT be edited.
config_config_file=$config_resources_dir/config_update.conf
# log options, set a log file to record backup log for restore use, this is can NOT be edited.
config_this_logfile=$WORKDIR/.update_backup.log
identity_file=~/.ssh/id_rsa.pub
# end


# check if user want to execute on remote clients
function parse_config_remote_execution()
{
    if [ -z "`eval $config_remote_execution`" ]; then
        echo_r "Error: config_remote_execution is NOT set, if you want execute it local, set it no, else set it yes. "
        exit 1
    elif [ x$config_remote_execution != x ];then
        case $config_remote_execution in
            yes|true|1)
                config_remote_execution=1
                ;;
            no|false|0)
                config_remote_execution=0
                ;;
            *)
                echo_r "Error: config_remote_execution has a bad set, please check and correct it. "
                exit 1
                ;;
        esac
    else
        echo_y "Can NOT find config_remote_execution, is it unset? Setting a default value for config_remote_execution. "
        config_remote_execution=0
    fi
}

function test_self(){
    # How to use this function:
    # First execute "$0 test_self", then execute "$0 update"

    echo_b "Test purpose begin. "

    # clean old test example
    echo_b "Clean old test example. "
    [ -d $WORKDIR/example_projects ] && rm -rf $WORKDIR/example_projects
    [ -d $WORKDIR/example_resources ] && rm -rf $WORKDIR/example_resources
    [ -d $WORKDIR/example_backup_dir ] && rm -rf $WORKDIR/example_backup_dir

    # make an example project directory
    if [ -z $config_project_dir -o ! -d $config_project_dir ]; then
        echo_b "Making an example project directory. "
        mkdir $WORKDIR/example_projects
        config_project_dir=example_projects
        # Padding example_projects directory
        touch $config_project_dir/example_filename
        mkdir $config_project_dir/example_directory
    fi

    # make an example resources directory
    if [ -z $config_resources_dir -o ! -d $config_resources_dir ]; then
        echo_b "Making an example resources directory. "
        mkdir  $WORKDIR/example_resources
        config_resources_dir=$WORKDIR/example_resources
    fi

    # make an example config_update.conf
    if [ -z $config_config_file -o ! -f $config_config_file ]; then
        echo_b "Making an example config_update.conf file. "
        touch $config_resources_dir/config_update.conf
        config_config_file=$config_resources_dir/config_update.conf
    # Padding config_update.conf file
    cat >$config_config_file <<eof
file    filename1          add
file    filename2          remove
file    filename3          update
file    filename4          add
config  cleancachea             enable
config  cleancacheb             disable
config  restartservicea         enable
config  restartserviceb         disable
target  192.168.1.241           ssh     22  root    yiCxVyW2DydhE
target  192.168.1.242           ssh     22  root    yiCxVyW2DydhE
target  192.168.1.243           ssh     22  root    yiCxVyW2DydhE
target  192.168.1.244           ssh     22  root    yiCxVyW2DydhE
eof
    files=`awk -F '[ ]+' '/^file/ { print $2 }' $config_config_file`
    echo_b "Making an example files(patches) refer to $config_config_file. "
    for names in $files; do
        [ ! -f $config_resources_dir/$names ] && touch $config_resources_dir/$names
    done
    fi

    # TODO
    # not ready for remote execution
    # test network and ssh for remote call

    # make an example backup directory
    if [ -z $config_backup_dir -o ! -d $config_backup_dir ]; then
        echo_b "Making an example backup directory"
        mkdir $WORKDIR/example_backup_dir
        config_backup_dir=$WORKDIR/example_backup_dir
    fi

    echo_g "Test purpose is finished and successfully! "
}

#function parse_config_file(){
#    # unbanned action
#    files=`awk -F '[ ]+' '/^file/ { print $2 }' $config_config_file`
#    configs=`awk -F '[ ]+' '/^config/ { print $2 }' $config_config_file`
#}

function ssh_keygen(){
    echo_b "generate SSH key and related files for itself."
    cd
    # Improvement
    # ssh-keygen parameters
    ssh-keygen -N "" -f /root/.ssh/id_rsa
    if [ $? -ne 0 ]; then
        echo_r "Error: generate SSH key and related files for itself failed! "
        exit 1
    fi
    cd ~/.ssh/
    [[ ! -e ~/.ssh/authorized_keys ]] && cp id_rsa.pub authorized_keys
    cd
    identity_file=~/.ssh/id_rsa.pub
}

# this action can NOT be replaced with check_ssh_connection function
function inject_ssh_key(){
# ssh-copy-id Line:41
which sshpass >/dev/null 2>&1 || yum -q -y install sshpass
if [ $? -ne 0 -a ! -f /etc/yum.repos.d/epel.repo ]; then
    echo_y "sshpass can NOT install on system with yum repolist, install epel first. "
    yum -q -y install http://dl.fedoraproject.org/pub/epel/6/x86_64/epel-release-6-8.noarch.rpm
    yum -q -y install sshpass
    if ! which sshpass >/dev/null 2>&1; then
        echo_r "Error: sshpass is can NOT install on system, please install it manually. "
        exit 1
    fi
fi

# inject ssh key for each host found in config files
hostname_list=$(awk -F '[ ]+' '/target/ {print $2}' $config_config_file)
for hostname in $hostname_list; do
    port=$(cat $config_config_file | awk -F '[ ]+' "/^target/ && /$hostname/ {print \$4}")
    user=$(cat $config_config_file | awk -F '[ ]+' "/^target/ && /$hostname/ {print \$5}")
    password=$(cat $config_config_file | awk -F '[ ]+' "/^target/ && /$hostname/ {print \$6}")
    # echo issue but it is less than ssh issue(It will report "Pseudo-terminal will not be allocated because stdin is not a terminal." when use stdin to ssh command.)
    sshpass -p $password ssh -p $port -oStrictHostKeyChecking=no $user@$hostname "exec sh -c 'echo $(cat ~/.ssh/id_rsa.pub) >> ~/.ssh/authorized_keys && (test -x /sbin/restorecon && /sbin/restorecon ~/.ssh ~/.ssh/authorized_keys >/dev/null 2>&1 || true)'"
    # sshpass issue: Pseudo-terminal will not be allocated because stdin is not a terminal.
    # to resolve this issue, do NOT give ssh command any stdin, sometimes "known host" maybe worked with this issue
    # Refer: http://unix.stackexchange.com/questions/151757/script-to-ssh-and-run-a-command-doesnt-work
    # Refer: http://stackoverflow.com/questions/305035/how-to-use-ssh-to-run-shell-script-on-a-remote-machine
    # comment this line
    #sshpass -p $password cat ~/.ssh/id_rsa.pub | ssh -T -p $port -oStrictHostKeyChecking=no $user@$hostname "exec sh -c 'cat >> ~/.ssh/authorized_keys && (test -x /sbin/restorecon && /sbin/restorecon ~/.ssh ~/.ssh/authorized_keys >/dev/null 2>&1 || true)'"
    if [ $? -eq 0 ]; then
        echo_g "SSH key inject to $hostname successfully! "
    else
        echo_r "SSH key inject to $hostname failed! "
        exit 1
    fi
done
}

# this action has some duplicates to inject_ssh_key function
function check_ssh_connection(){
    hostname_list=$(awk -F '[ ]+' '/target/ {print $2}' $config_config_file)
    for hostname in $hostname_list; do
        port=$(cat $config_config_file | awk -F '[ ]+' "/^target/ && /$hostname/ {print \$4}")
        user=$(cat $config_config_file | awk -F '[ ]+' "/^target/ && /$hostname/ {print \$5}")
        password=$(cat $config_config_file | awk -F '[ ]+' "/^target/ && /$hostname/ {print \$6}")
        if ! ssh -i ~/.ssh/id_rsa -p $port -oPasswordAuthentication=no $user@$hostname "exec sh -c 'true'" >/dev/null 2>&1; then
            echo_b "Can NOT login $hostname through SSH key ~/.ssh/id_rsa, retry to inject SSH keys. "
            sshpass -p $password ssh -p $port -oStrictHostKeyChecking=no $user@$hostname "exec sh -c 'echo $(cat ~/.ssh/id_rsa.pub) >> ~/.ssh/authorized_keys && (test -x /sbin/restorecon && /sbin/restorecon ~/.ssh ~/.ssh/authorized_keys >/dev/null 2>&1 || true)'"
            if [ $? -ne 0 ]; then
                echo_r "Error: SSH key inject to $hostname failed! "
                exit 1
            else
                echo_g "SSH key inject to $hostname successfully! "
                if ssh -p $port -oStrictHostKeyChecking=no $user@$hostname "exec sh -c 'cat ~/.ssh/authorized_keys | sort | uniq --repeated | grep ssh'"; then
                    echo_y "Duplicate lines found in ~/.ssh/authorized_keys, remove them. "
                    ssh -p $port -oStrictHostKeyChecking=no $user@$hostname "exec sh -c 'cat ~/.ssh/authorized_keys | sort | uniq > ~/.ssh/authorized_keys~;\mv ~/.ssh/authorized_keys~ ~/.ssh/authorized_keys'"
                    if [ $? -eq 0 ]; then
                        echo_g "Duplicate lines found in ~/.ssh/authorized_keys removed successfully! "
                    else
                        echo_y "Duplicate lines found in ~/.ssh/authorized_keys removed failed! "
                    fi
                else
                    echo_g "SSH connection to $hostname is ok! "
                fi
            fi
        else
            echo_g "SSH connection to $hostname is ok! "
        fi
    done
}

function do_cp(){
    SOURCE=$1
#    echo "var: $SOURCE"
#    echo "result: $(dirname $SOURCE | grep ^\/ | awk '{print substr($1,1,1)}' )"
#    exit 0
    if test "$(dirname $SOURCE | grep ^\/ | awk '{print substr($1,1,1)}')" == ""; then
        echo_b "Execute copy action. "
        DEST=$config_project_dir/$SOURCE
        \cp $SOURCE $DEST
    else
        echo_y "Self test purpose found! But we can do this action! "
        [ ! -d $config_project_dir/$(dirname $SOURCE) ] && mkdir -p $config_project_dir/$(dirname $SOURCE)
        \cp $SOURCE $config_project_dir/$(dirname $SOURCE)
    fi
}
function do_remove(){
    FILE=$1
    if test "$(dirname $SOURCE | awk -F '/' '{print $1}')" == ""; then
        rm -rf $config_project_dir/$FILE
    else
        echo_y "Self test purpose found! This can NOT do remove action on self test purpose, skipping..."
        return
    fi

}

# TODO
# not ready for remote execution
# for remote call
#function do_remote_cp(){}
#function fo_remote_remove(){}

function file_operation(){
    echo_b "Begin files operations"
    files=`awk -F '[ ]+' '/^file/ { print $2 }' $config_config_file`
    for names in $files; do
        if grep $names $config_config_file | grep add >/dev/null 2>&1 ; then
            # do_cp
            do_cp $names
        elif grep $names $config_config_file | grep update >/dev/null 2>&1 ;then
            # do_cp
            do_cp $names
        elif grep $names $config_config_file | grep remove >/dev/null 2>&1 ;then
            # do_remove
            do_remove $names
        else
            exit 1
        fi
    done
    echo_g "Files operations finished successfully! "
}

# TODO
# no example here, please refer to your real production environment
#function do_clean_cache(){}
#function do_restart_service(){}

function service_operation(){
    echo_b "Begin services operations"
    configs=`awk -F '[ ]+' '/^config/ { print $2 }' $config_config_file`
    for names in $configs; do
        if grep $names $config_config_file | grep cleancache | grep enable >/dev/null 2>&1 ; then
            # do_clean_cache
            echo do_clean_cache $names
        elif grep $names $config_config_file | grep cleancache | grep disable >/dev/null 2>&1 ; then
            # echo a warning
            echo_y "Warning: disable action is NOT recommended, $names skipped."
        elif grep $names $config_config_file | grep restartservice | grep enable >/dev/null 2>&1 ; then
            # do_restart_service
            echo do_restart_service $names
        elif grep $names $config_config_file | grep restartservice | grep disable >/dev/null 2>&1 ; then
            # echo a warning
            echo_y "Warning: disable action is NOT recommended, $names skipped."
        else
            echo $names
            echo_r "Error: Wrong config file $config_config_file, please check it. "
            exit 1
        fi
    done
    echo_g "Services operations finished successfully! "
}

function check_remote_server_status(){
    # TODO
    # not ready for remote execution
    # for remote call
    echo

}

function backup(){
    echo_b "Backup files before update"
#    backup_filename=backup_$(date +%F_%H_%M_%S).tgz
    backup_filename=backup_$(date +%Y_%m_%d_%H_%M_%S).tgz
    # tar directory
    cd $config_project_dir/..
    tar --create --gzip --absolute-names --file=$config_backup_dir/$backup_filename $config_project_dir
    if [ $? -eq 0 ]; then
        echo_g "Backup files before update finished and successfully! "
        echo "restore_least_file=$config_backup_dir/$backup_filename" > $config_this_logfile
    else
        echo_r "Error: Backup files before update failed! Please alter to administrator. "
        exit 1
    fi

}

function restore(){
    echo_b "Restore files for rollback"
    if [ -f $config_this_logfile ]; then
        . $config_this_logfile
    fi
    restore_least_file=${restore_least_file:-1}
    if [ -s $restore_least_file ]; then
        tar -C $config_project_dir/.. -zxf $restore_least_file
        if [ $? -eq 0 ]; then
            echo_g "Restore files finished and successfully! "
        else
            echo_r "Restore files failed! Please alter to administrator. "
            exit 1
        fi
    else
        echo_r "Can NOT find backup files in $config_backup_dir, backup once indeed? "
        exit 1
    fi

}

# TODO
# not ready for remote execution
# for remote call
# function remote_backup(){}
# function remote_restore(){}


function rollback(){
    echo_b "rollback after update failed"
    $0 restore

    echo_g "rollback finished and successfully! "
}

function update_status(){
    # TODO
    # no example here, please refer to your real production environment
    # check if update success or failure
    echo update_status
    # if failure, do rollback action
        # service_operation
}

# Put check_dependencies in front of update function
function check_dependencies(){
    echo_b "Checking dependencies for update procedure. "

    if [ -z $config_project_dir ]; then
        echo_r "Error: config_project_dir is undefined! "
        exit 1
    fi

    if [ ! -d $config_resources_dir ]; then
        echo_r "Error: config_resources_dir is undefined! "
    fi

    if [ -z $config_config_file ]; then
        echo_r "Error: config_config_file is undefined! "
        exit 1
    fi

    left_disk_space=`df $config_backup_dir | tail -n1 | awk '{print $(NF -2)}'`
    # set 2097152 to project directory size
    if [ -z $config_project_dir -o ! -d $config_project_dir ]; then
        project_file_space_usage=$(du -s /root | awk '{print $1}')
        required_size=$(expr $project_file_space_usage \* 2)
    fi
    if [[ $left_disk_space -lt $required_size ]]; then
        echo_r "Disk space of $config_backup_dir is smaller than $required_size. "
        exit 1
    fi

    if [ ! -f /root/.ssh/id_rsa ]; then
        ssh_keygen
    fi

    echo_g "All required dependencies check pass! "

}

function update(){
    # TODO
    # thinking carefully with all exit status, which is not good for automatic update 
    check_dependencies
    backup
    file_operation
    service_operation
    update_status
}

function destroy() {
    # echo a warning message
    echo_y "Warning: This action will destroy all this project, and this is unrecoverable! "
    answer="n"
    echo_y "Do you want to destroy this project? "
    read -p "(Default no,if you want please input: y ,if not please press the enter button):" answer
    case "$answer" in
        y|Y|Yes|YES|yes|yES|yEs|YeS|yeS )
        # delete all file expect for this script self
        # find: warning: Unix filenames usually don't contain slashes (though pathnames do).  That means that '-name `./deploy.sh'' will probably evaluate to false all the time on this system.  You might find the '-wholename' test more useful, or perhaps '-samefile'.  Alternatively, if you are using GNU grep, you could use 'find ... -print0 | grep -FzZ `./deploy.sh''.
            # echo $WORKDIR/
            #find -L $WORKDIR -type f ! -name "$(basename $0)" -exec ls --color=auto -al {} \;
            # find -L . -type f ! -name "deploy.sh" -exec ls --color=auto -al {} \;
            # find -L . -type d -exec ls --color=auto -al {} \;
            # find -L ./ -maxdepth 1 ! -name "deploy.sh" ! -wholename "./"
        # ls | grep -v "fielname" |xargs rm -rf
        find -L $WORKDIR -maxdepth 1 ! -name "$(basename $0)" ! -wholename "$WORKDIR"  -exec rm -rf {} \;
        if [ $? -eq 0 ];then
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

case $1 in
    update)
        update
        ;;
    backup)
        backup
        ;;
    restore)
        restore
        ;;
    rollback)
        rollback
        ;;
    destroy)
        destroy
        ;;
    help|*)
        echo "Usage: $0 {update|backup|restore|rollback|destroy} with $0 itself"
        exit 1
        ;;
esac

# This is not essential with 'case .. esac' handled no args excutions
# replace "exit 0" with ":"
#exit 0
: