#!/usr/bin/env bash
# remove old app files, not restrict, NO QA
set -o errexit
apps_dir="/opt/ebt/apps"
current_pwd=$(pwd)
if [[ ${current_pwd} != ${apps_dir} ]]; then
    cd apps_dir
fi
app_list="
appname1
appname2
appname3
"

current_app_list=$(ls -1 .)

for app in ${app_list};do
    if [[ ${current_app_list} =~ ${app} ]]; then # if echo "${strings}" | grep ${string}; then
        app_count=$(ls -t . | grep ${app}| wc -l)
        if [[ ${app_count} > 2 ]]; then
            app_count=$(expr ${app_count} - 2 ) # app_count=$((app_count-2))
        fi
        echo "Found:$app, Old files count:$app_count"
        ls -t . | grep ${app} | tail -${app_count} | xargs rm -rf
    fi
done
