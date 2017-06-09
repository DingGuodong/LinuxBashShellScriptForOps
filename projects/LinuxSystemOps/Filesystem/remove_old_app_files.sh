#!/usr/bin/env bash
# remove old app files, not restrict, NO QA
#set -o errexit
#set -o xtrace
apps_dir="/opt/ebt/apps"
current_pwd=$(pwd)
if [[ ${current_pwd} != ${apps_dir} ]]; then
    cd ${apps_dir}
fi
app_list="
agent-management
dataexchange
ebtdatres
erisk
erp
policy
proposal
user
"

current_app_list=$(ls -1 .)

# IFS=' '$'\t'$'\n', IFS=$' \t\n', If IFS is unset, or its value is exactly <space><tab><newline>
old_IFS=$IFS
IFS=' '$'\t'$'\n'

for app in ${app_list};do
    if echo "$current_app_list" | grep ${app} >/dev/null 2>&1; then #if [[ ${current_app_list} =~ ${app} ]]; then
        all_app_count=$(ls -t . | grep ${app}| wc -l)
        if [[ ${all_app_count} > 2 ]]; then
            old_app_count=$(expr ${all_app_count} - 2 ) # old_app_count=$((all_app_count-2))
            echo "Found:$app, Old files count:$old_app_count"
            ls -t . | grep ${app} | tail -${old_app_count} | xargs rm -rf
        fi
    fi
done

IFS="$old_IFS"
