#!/usr/bin/env bash
lock=/var/lock/subsys/lock
if [ ! -e ${lock} ]; then
    trap " rm -f ${lock}; exit" INT TERM EXIT
    touch ${lock}
    #critical-section
    rm ${lock}
    trap - INT TERM EXIT
else
    echo "critical-section is already running"
fi
