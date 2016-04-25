#!/bin/bash

# What it can be done?
# If you work with fixed hours, you can use this script find out 
# when you can go home or go shopping with your friends.
# Please feel free to using it and share to your friends.
# :)


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
    # cecho -yellow sometext  # Warnning
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
    # Warnning
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

# define 
open_time=11:08
work_time=9.5
close_time=18:38
least_time=06:00
last_time=23:59
late_time=10:00
worked_time=2.4
# end define

function validate_input_time(){
    if [[ $# -ne 1 ]]; then
        echo "Bad line, need 1 parameter at least! "
        exit 1
    fi
    input_time=$1
    echo $input_time | grep -E "^([0-9]|0[0-9]|1[0-9]|2[0-3]):([0-5][0-9])$" >/dev/null 2>&1
    rc=$?
    if [[ $rc -ne 0 ]]; then
        echo "Bad input time"
        exit 1
    fi
    return $rc
}

function mintues_to_seconds(){
    if [[ $# -ne 1 ]]; then
        echo "Bad line, need 1 parameter at least! "
        exit 1
    fi
    return 0
}

function hours_to_minutes(){
    if [[ $# -ne 1 ]]; then
        echo "Bad line, need 1 parameter at least! "
        exit 1
    fi
    hours=`echo $1 | awk -F ':' '{print $1}'`
    minutes=`echo $1 | awk -F ':' '{print $2}'`
    total_minutes=`echo "$hours * 60 + $minutes" | bc`
    if [[ $? -eq 0 && $total_minutes != "" && $total_minutes -ge 0 ]]; then
        # here can NOT use a return
        echo $total_minutes
    else
        echo "Exception occurs! "
        exit 1
    fi
}


function validate_late_to_work(){
    least_minutes=$(hours_to_minutes $least_time)
    last_minutes=`hours_to_minutes $last_time`
    late_minutes=`hours_to_minutes $late_time`
    open_minutes=`hours_to_minutes $open_time`
    if [ $open_minutes -lt $least_minutes ] || [ $open_minutes -gt $late_minutes ]; then
        echo "You are late! "
        exit 1
    fi
}

function computing_close_time(){
    open_minutes=`hours_to_minutes $open_time`
    close_minutes=`echo "$work_time * 60 + $open_minutes" | bc`
    close_hours=`echo "$close_minutes / 60" | bc`
    close_minutes=`echo "$close_minutes % 60" | bc | awk -F '.' '{print $1}'`
    close_time="$close_hours:$close_minutes"
    echo $close_time
}

function computing_worked_hours(){
    open_minutes=`hours_to_minutes $open_time`
    now_time=$(date +%H:%M)
    now_minutes=`hours_to_minutes $now_time`
    worked_minutes=`echo "$now_minutes - $open_minutes" | bc`
    worked_hours=`echo "$worked_minutes / 60" | bc`
    echo $worked_hours
}

function computing_worked_minutes(){
    open_minutes=`hours_to_minutes $open_time`
    now_time=$(date +%H:%M)
    now_minutes=`hours_to_minutes $now_time`
    worked_minutes=`echo "$now_minutes - $open_minutes" | bc`
    worked_minutes=`echo "$worked_minutes % 60" | bc | awk -F '.' '{print $1}'`
    echo $worked_minutes
}

function work_report(){
    echo "================================================================"
    echo -e "You start work at \033[32m$open_time\033[0m."
    echo -e "You need work \033[32m$work_time\033[0m hours for your salary."
    echo -e "You can leave at \033[32m$(computing_close_time)\033[0m."
    echo -e "now time is \033[32m$(date +%H:%M)\033[0m."
    echo -e "You have worked \033[32m$(computing_worked_hours)\033[0m hours and \033[32m$(computing_worked_minutes)\033[0m minutes."
    echo "================================================================"
}

function read_user_input(){
    read -p "please input your open time, such as 09:00(default): " open_time
    if [[ "$open_time" == "" ]]; then
        open_time="09:00"
    fi
}

function main(){
    read_user_input
    validate_input_time $open_time
    validate_late_to_work $open_time
    work_report
}

main
