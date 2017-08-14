#!/usr/bin/env bash
# Created by PyCharm.
# File:                 LinuxBashShellScriptForOps:get_cpu_usage_idle.sh
# User:                 Guodong
# Create Date:          2017/8/14
# Create Time:          10:32
# Function:             get cpu idle percentage of certain program
# Note:                 
# Prerequisite:         sed, awk, vmstat, top, etc
# Description:          get cpu idle percentage of certain program
# Reference:            Getting cpu usage realtime
#                       https://askubuntu.com/questions/274349/getting-cpu-usage-realtime
#                       How does ps aux | grep '[p]attern' exclude grep itself?
#                       https://stackoverflow.com/questions/20528894/how-does-ps-aux-grep-pattern-exclude-grep-itself



daemon_name="dockerd"  # the program name to check out

daemon_name_to_search_pid=$(echo ${daemon_name} | sed "s/\([a-z]\{1\}\)\(.*\)/\[\1\]\2/g")
pid_to_trace=$(ps -ef | grep ${daemon_name_to_search_pid} | awk 'NR==1{print $2}')

if "x$pid_to_trace" == "x"; then
    echo "pid can NOT be found"
    exit 1
fi

cpu_idle_percentage_threshold=10
keep_running_flag=1

while [[ ${keep_running_flag} -eq 1 ]]; do
    cpu_idle=$(vmstat 1 2|tail -1|awk '{print $15}')
    if [[ ${cpu_idle} -lt ${cpu_idle_percentage_threshold} ]]; then
        date --rfc-2822
        echo "CPU idle percentage is too small!"
        vmstat 1 5
        top -bn 2 -d 0.01 -p ${pid_to_trace}
        keep_running_flag=0
    fi
done
: