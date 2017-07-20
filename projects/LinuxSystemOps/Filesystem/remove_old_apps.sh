#!/usr/bin/env bash
# filename: remove_old_app.sh
# remove old apps, not restrict
# 59 17 * * * /bin/bash --login /opt/ebt/apps/remove_old_apps.sh >>/tmp/remove_old_apps.log
#set -o errexit
#set -o xtrace
apps_dir="/opt/ebt/apps"  # apps dir to clear
app_list="
agent-management
agent-stats
canal-to-kafka
cashier
customer
dataexchange
ebtdatres
erisk
erp
insiap
insure-validation
message
policy
proposal
resource
risk-market
sms
user
zyj-touch
"

current_pwd=$(pwd)  # crontab maybe can not recognize $PWD or `pwd` if without 'bash --login', need a test
if [[ ${current_pwd} != ${apps_dir} ]]; then
    cd ${apps_dir}
fi

current_app_list=$(ls -1 .)

# IFS=' '$'\t'$'\n', IFS=$' \t\n', If IFS is unset, or its value is exactly <space><tab><newline>
old_IFS=$IFS
IFS=' '$'\t'$'\n'

for app in ${app_list};do
    all_app_count=0
    old_app_count=0
    if echo "$current_app_list" | grep ${app} >/dev/null 2>&1; then #if [[ ${current_app_list} =~ ${app} ]]; then
        all_app_count=$(ls -t . | grep ${app}| wc -l)
        if [[ ${all_app_count} -gt 2 ]]; then # Note: do NOT use '>', use '-gt' in '[[ EXPRESSION ]]' instead
            old_app_count=$(expr ${all_app_count} - 2 ) # old_app_count=$((all_app_count-2))
            echo "Info: Found:$app, Total files count: $all_app_count, Old files count: $old_app_count, clean them"
#            ls -dt ./* | grep ${app} | tail -${old_app_count} | xargs ls -dl
            ls -dt ./* | grep ${app} | tail -${old_app_count} | xargs rm -rf
         else
            echo "Warning: Found:$app, Total files count: $all_app_count, pass"
        fi
    else
        echo "Error: $app not found! "
    fi
done

IFS="$old_IFS"

echo "Info: Clean Finished! "
