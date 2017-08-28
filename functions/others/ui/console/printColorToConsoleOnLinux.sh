#!/usr/bin/env bash
# Created by PyCharm.
# File:                 LinuxBashShellScriptForOps:${NAME}.sh
# User:                 Guodong
# Create Date:          2017/8/28
# Create Time:          12:02
# Function:             
# Note:                 
# Prerequisite:         
# Description:          
# Reference:            coreutils:ls.c
function red(){
    # Color red
    [ $# -ne 1 ] && return 1
    echo -e "\033[31m$1\033[0m"
}

function red_bright (){
    # Color bright red
    [ $# -ne 1 ] && return 1
    echo -e "\033[01;31m$1\033[0m"
}

function green (){
    # Color green
    [ $# -ne 1 ] && return 1
    echo -e "\033[32m$1\033[0m"
}

function green_bright (){
    # Color bright green
    [ $# -ne 1 ] && return 1
    echo -e "\033[01;32m$1\033[0m"
}

function yellow (){
    # Color yellow
    [ $# -ne 1 ] && return 1
    echo -e "\033[33m$1\033[0m"
}

function yellow_bright (){
    # Color bright yellow
    [ $# -ne 1 ] && return 1
    echo -e "\033[01;33m$1\033[0m"
}

function blue (){
    # Color blue
    [ $# -ne 1 ] && return 1
    echo -e "\033[34m$1\033[0m"
}

function blue_bright (){
    # Color bright blue
    [ $# -ne 1 ] && return 1
    echo -e "\033[01;34m$1\033[0m"
}

function magenta (){
    # Color purple,magenta
    [ $# -ne 1 ] && return 1
    echo -e "\033[35m$1\033[0m"
}

function magenta_bright (){
    # Color bright purple,magenta
    [ $# -ne 1 ] && return 1
    echo -e "\033[01;35m$1\033[0m"
}

function cyan (){
    # Color cyan
    [ $# -ne 1 ] && return 1
    echo -e "\033[36m$1\033[0m"
}

function cyan_bright (){
    # Color bright cyan
    [ $# -ne 1 ] && return 1
    echo -e "\033[01;36m$1\033[0m"
}