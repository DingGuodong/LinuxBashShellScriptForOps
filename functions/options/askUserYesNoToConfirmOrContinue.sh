#!/usr/bin/env bash
# Created by PyCharm.
# File:                 LinuxBashShellScriptForOps:askUserYesNoToConfirmOrContinue.sh
# User:                 Guodong
# Create Date:          2017/7/19
# Create Time:          15:26
# Function:             
# Note:                 
# Prerequisite:         
# Description:          ask user yes or no to confirm or continue in bash
# Reference:            /usr/share/yum-cli/cli.py
#                       /usr/share/yum-cli/output.py
#                       /usr/lib/python2.7/site-packages/yum/plugins.py

function confirm_continue(){
    echo "Is this ok? "
    read -n 1 -r -p "Enter the y or Y to continue:" user_answer  # read -n1 -r -p "Press any key to continue..." key
    if [[ "${user_answer}" != "y" ]] && [[ "${user_answer}" != "Y" ]]; then
        echo -e "\n\nExiting on user cancel."  # exiting because "Download Only" specified
        exit 1
    else
        echo
    fi
}

confirm_continue
# main job
echo "foo"
