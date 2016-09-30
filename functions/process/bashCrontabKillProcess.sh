#!/usr/bin/env bash
# purpose&goal&demand: tail -f <file>, exit after 2 seconds
sleep_seconds=2
pid_this=$$
if [[ "x$1" == "x" && -f $1 ]]; then
    echo "missing parameter..."
    exit 1
else
    GID=`ps -o pid,ppid,pgid,gid,sess,cmd -U root | grep "$0" | grep "$$" | awk '{print $5}'| sort | uniq `
    sleep ${sleep_seconds} &&  pkill -9 -G ${GID} &
    # TODO(Guodong Ding) big TODO: bug here, parent pid exit but child pid exist by init received, and others
    # Unstoppable Zombie Processes in docker
    # linux kill defunct process in docker
    tail -f $1
    wait
fi
