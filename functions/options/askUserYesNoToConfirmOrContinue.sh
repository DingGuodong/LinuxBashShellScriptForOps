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
# Reference:            

read -n1 -r -p "Enter the y or Y to continue:" user_answer  # read -n1 -r -p "Press any key to continue..." key
if [ "${user_answer}" != "y" ] && [ "${user_answer}" != "Y" ]; then
    echo
    exit 1
else
    echo
fi

# main job
echo "foo"