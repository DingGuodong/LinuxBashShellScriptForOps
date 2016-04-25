#!/bin/bash
function cecho {
        while [ "$1" ]; do
                case "$1" in 
                        -normal)        color="\033[00m" ;;
-black)         color="\033[30;01m" ;;
-red)           color="\033[31;01m" ;;
-green)         color="\033[32;01m" ;;
-yellow)        color="\033[33;01m" ;;
-blue)          color="\033[34;01m" ;;
-magenta)       color="\033[35;01m" ;;
-cyan)          color="\033[36;01m" ;;
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

