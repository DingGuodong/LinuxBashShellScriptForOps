#!/usr/bin/env bash
lock=/var/lock/subsys/lock
if ( set -o noclobber; echo "$$" > "$lock") 2> /dev/null;then
    trap 'rm -f "$lock"; exit $?' INT TERM EXIT
    critical-section
    rm -f "$lock"
    trap - INT TERM EXIT
else
    echo "Failed to acquire lock: $lock"
    echo "held by $(cat ${lock})"
fi