#!/bin/sh

# refer to: https://raw.githubusercontent.com/springlie/cecho/master/cecho.sh

cecho()
{
    #FOREGROUND

    local FG_BLACK="\e[30m"
    local FG_RED="\e[31m"
    local FG_GREEN="\e[32m"
    local FG_YELLOW="\e[33m"
    local FG_BLUE="\e[34m"
    local FG_PURPLE="\e[35m"
    local FG_CYAN="\e[36m"
    local FG_WHITE="\e[37m"

    #BACKGROUND

    local BG_BLACK="\e[40m"
    local BG_RED="\e[41m"
    local BG_GREEN="\e[42m"
    local BG_YELLOW="\e[43m"
    local BG_BLUE="\e[44m"
    local BG_PURPLE="\e[45m"
    local BG_CYAN="\e[46m"
    local BG_WHITE="\e[47m"

    #ACTION

    local DONE="\e[0m"
    local HIGHLIGHT="\e[1m"
    local UNDERLINE="\e[4m"
    local BLINK="\e[5m"
    local REVERSE="\e[7m"
    local INVISIBLE="\e[8m"

}