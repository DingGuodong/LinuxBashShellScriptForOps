#!/usr/bin/env bash
# Program name: pstree2
# Usage: bash $0 <pid>
# Description: show the cmdline of the recursively by its ppid,
#   like the `pstree` display a tree of processes but only show related items.
# Author: dgden
# Create Date: 2021/5/10
# Create Time: 22:24


#if [ "$(id -u)" != "0" ]; then
#  echo "WARNING: This script should be run as root" 2>&1
#fi

[[ "$1" == "" ]] && echo "usage: show the ppid recursively of the pid, using with \"$0 <pid>\"" && exit 1

current_pid="$1"

# shellcheck disable=SC2001
current_pid_grep=$(echo "$current_pid" | sed 's/^\(.\)/[\1]/')

# shellcheck disable=SC2009
ps -ef | grep "$current_pid_grep" | awk -v pid="$current_pid" '$2==pid' | grep "$current_pid_grep"

# shellcheck disable=SC2009
current_ppid="$(ps -ef | grep "$current_pid_grep" | awk -v ppid="$current_pid" '$2==ppid {print $3}')"

if [[ "$current_ppid" == "" || "$current_ppid" == "0" ]]; then
    echo "the pid not exists."
    exit 1
fi

while [[ $current_ppid -ne 1 ]]; do
  # shellcheck disable=SC2001
  current_ppid_grep=$(echo "$current_ppid" | sed 's/^\(.\)/[\1]/')
  # shellcheck disable=SC2009
  ps -ef | grep "$current_ppid_grep" | awk -v pid="$current_ppid" '$2==pid'

  # shellcheck disable=SC2009
  current_ppid="$(ps -ef | grep "$current_ppid_grep" | awk -v ppid="$current_ppid" '$2==ppid {print $3}')"
  if [[ $current_ppid -eq 1 ]]; then
    break
  fi
done