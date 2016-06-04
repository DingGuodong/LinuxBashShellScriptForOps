#!/bin/bash

# Public header
# =============================================================================================================================
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
if [ ! ${one_line} ]; then
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

WORKDIR=${PRGDIR}
# end public header
# =============================================================================================================================

# Where to get source code
SOURCEURL=https://github.com/DingGuodong/GitOSCAutoDeploy.git

# Setting how many days do you want save old releases, default is 10 days
save_old_releases_for_days=10

function setDirectoryStructure() {
    if [ -f ${WORKDIR}/.lock ];then
        echo_g "Set directory structure has been done, skipping. "
        return
    fi
    echo_b "Setting directory structure."
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
    # revisions.log is used to log every deploy or rollback. Each entry is timestamped and the executing user (username from local machine) is listed. Depending on your VCS data like branchnames or revision numbers are listed as well.
    # shared contains the linked_files and linked_dirs which are symlinked into each release. This data persists across deployments and releases. It should be used for things like database configuration files and static and persistent user storage handed over from one release to the next.
    # The application is completely contained within the path of :deploy_to. If you plan on deploying multiple applications to the same server, simply choose a different :deploy_to path.

    # Check directories for deploy
    # [ ! -d ${WORKDIR}/current ] && mkdir ${WORKDIR}/current
    [ ! -d ${WORKDIR}/release ] && mkdir ${WORKDIR}/release
    [ ! -d ${WORKDIR}/repository ] && mkdir ${WORKDIR}/repository
    [ ! -d ${WORKDIR}/share ] && mkdir ${WORKDIR}/share
    # end directories structure
    touch ${WORKDIR}/.lock
    echo_g "Set directory structure successfully! "
}

function checkDependencies() {
    echo_b "Checking dependencies for deploy procedure. "
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
    if [[ -z ${SOURCEURL} ]]; then
        echo_r "Error: SOURCEURL is undefined! "
        exit 1
    fi
    DISKSPACE=`df ${WORKDIR} | tail -n1 | awk '{print $(NF -2)}'`
    if [[ ${DISKSPACE} -lt 2097152 ]]; then
        echo_y "Warning: Disk space of ${WORKDIR} is smaller than 2GB"
        #exit 1
    fi

    echo_g "All required dependencies check pass! "

}

function cleanOldReleases(){
    save_days=${save_old_releases_for_days:-10}
    if [ ! -d ${WORKDIR}/release ]; then
        echo_b "Can NOT find release directory, skipping . "
        return
    fi
    need_clean=$(find ${WORKDIR}/release -mtime +${save_days} -exec ls '{}' \;)
    if [ ! -z ${need_clean} ]; then
        echo_g "Expired releases found and will be removed from project! "
        find ${WORKDIR}/release -mtime +${save_days} -exec rm -rf '{}' \;
        if [ $? -eq 0 ]; then
            echo_g "Expired releases have removed from project! "
        else
            echo_r "Can NOT remove expired releases, please alter to Admin users. "
        fi
    else
        echo_g "All releases are not expired, skipping. "
    fi


}
function deploy() {
    # check a directories lock, Note: this is redundant
    if [[ ! -f ${WORKDIR}/.lock ]]; then
        setDirectoryStructure
    fi
    cleanOldReleases
    checkDependencies
    # Make directory to release directory
    SOURCEDIR="${WORKDIR}/release/$(date +%Y%m%d%H%M%S)"
    [ ! -d ${SOURCEDIR} ] && mkdir ${SOURCEDIR}

    # Get files from source code repository
    git clone ${SOURCEURL} ${SOURCEDIR}
    # svn co http://$SOURCEURL ${WORKDIR}/repository

    # TODO
    # get branchnames or revision numbers from VCS data


    # Remove .git or .svn
    [ -d ${SOURCEDIR}/.git ] && rm -rf ${SOURCEDIR}/.git
    [ -d ${SOURCEDIR}/.svn ] && rm -rf ${SOURCEDIR}/.svn

    # ifdef Complie
    # endif

    # Make source code symbolic link to current
    ( [ -f ${WORKDIR}/current ] || [ -d ${WORKDIR}/current ] ) && rm -rf ${WORKDIR}/current
    ln -s ${SOURCEDIR} ${WORKDIR}/current

    # Move conf and logs directories from release to share
    [ -d ${WORKDIR}/release/conf ] && mv ${WORKDIR}/release/conf ${WORKDIR}/share/conf
    [ -d ${WORKDIR}/release/logs ] && mv ${WORKDIR}/release/logs ${WORKDIR}/share/logs

    # Make conf and logs symbolic link to current
    [ -d ${WORKDIR}/share/conf ] && ln -s ${WORKDIR}/share/conf ${WORKDIR}/current/conf
    [ -d ${WORKDIR}/share/logs ] && ln -s ${WORKDIR}/share/logs ${WORKDIR}/current/logs

    # Start service or validate status
    if [[ -e ${WORKDIR}/current/bin/startup.sh ]]; then
        ${WORKDIR}/current/bin/startup.sh start
        retval=$?
    else
        # TODO
        # external health check
        retval=0
    fi
    retval=$?

    # if started ok, then create a workable program to a file
    if [[ ${retval} -eq 0 ]]; then
    # Note cat with eof must start at row 0, and with eof end only, such as no blank spaces, etc
    cat >${WORKDIR}/share/workable_program.log <<eof
${SOURCEDIR}
eof
    echo_g "Deploy successfully! "
    echo_g "current workable version is $(cat ${WORKDIR}/share/workable_program.log)"
    ls --color=auto -l ${WORKDIR}/current
    else
        echo_r "Error: Deploy failed! "
        $0 rollback
    fi
}

# Rollback to last right configuraton
function rollback() {
    # The key is find last files which can work
    WORKABLE_PROGRAM=`cat ${WORKDIR}/share/workable_program.log`
    if [[ -z WORKABLE_PROGRAM ]]; then
        echo_r "Error: Can NOT find workable release version! Please check if it is first deployment! "
        exit 1
    fi
    # # Stop service
    if [[ -e ${WORKDIR}/current/bin/startup.sh ]]; then
        ${WORKDIR}/current/bin/startup.sh stop
    fi

    # Remove failed deploy
    rm -rf ${WORKDIR}/current

    # Remake source code symbolic link to current
    ln -s ${WORKABLE_PROGRAM} ${WORKDIR}/current

    # Remake conf and logs symbolic link to current
    [ -d ${WORKDIR}/share/conf ] && ln -s ${WORKDIR}/share/conf ${WORKDIR}/current
    [ -d ${WORKDIR}/share/logs ] && ln -s ${WORKDIR}/share/logs ${WORKDIR}/current

    # Start service or validate status
    if [[ -e ${WORKDIR}/current/bin/startup.sh ]]; then
        ${WORKDIR}/current/bin/startup.sh start
        retval=$?
    else
        # TODO
        # external health check
        retval=0
    fi
    retval=$?

    # if started ok, then create a workable program to a file
    if [[ ${retval} -eq 0 ]]; then
        echo_g "Rollback successfully! "
        echo_g "current workable version is $WORKABLE_PROGRAM"
        ls --color=auto -l ${WORKDIR}/current
    fi
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
            # echo ${WORKDIR}/
            #find -L ${WORKDIR} -type f ! -name "$(basename $0)" -exec ls --color=auto -al {} \;
            # find -L . -type f ! -name "deploy.sh" -exec ls --color=auto -al {} \;
            # find -L . -type d -exec ls --color=auto -al {} \;
            # find -L ./ -maxdepth 1 ! -name "deploy.sh" ! -wholename "./"
        # ls | grep -v "fielname" |xargs rm -rf
        find -L ${WORKDIR} -maxdepth 1 ! -name "$(basename $0)" ! -wholename "${WORKDIR}"  -exec rm -rf '{}' \;
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

# Just a test for call itself, comment it
# if [[ $# -lt 1 ]]; then
#   $0 help
#   exit
# fi
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

# This is not essential with 'case .. esac' handled no args excutions
# replace "exit 0" with ":"
#exit 0
: