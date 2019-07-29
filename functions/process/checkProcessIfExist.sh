#!/usr/bin/env bash
PIDFILE=""
# about "kill -0 <pid>", see man 2 kill
# If sig is 0, then no signal is sent, but error checking is still performed;
# this can be used to check for the existence of a process ID or process group ID.
if test -s  ${PIDFILE}; then
    if ! kill -0 "$(cat ${PIDFILE})" >/dev/null 2>&1; then
        echo xxx
    fi
else
     echo "PID file could not be found!"
     exit 1
fi
