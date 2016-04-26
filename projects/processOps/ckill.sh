#!/bin/bash
# Stopping process abruptly using kill
COMMAND=$1
USER=$2
if [[ -z "$COMMAND" ]]; then
    echo "Fatal error, list of command names must follow $0"
    exit 1
fi
if [[ "$1" == "-h" ||  "$1" == "--help" ]]; then
    echo "Func: This shell script will find the process you want to kill with signal 9, process name support regular expression with 'grep'"
    echo "Usage: $0 command [username]"
    echo "Example: $0 command, this will kill all process which match 'command'"
    exit 0
fi
if [[ -z "$USER" ]]; then
    USER=root
fi
pid="`ps aux | grep "$COMMAND" | grep "$USER" | grep -v grep | awk '{print $2}'`"
if [[ -z "$pid" ]]; then
    echo ":( , can NOT find $COMMAND running by $USER"
    exit 1
fi
kill -9 "$pid" >/dev/null 2>&1
retval=$?
pid=`ps aux | grep "$COMMAND" | grep "$USER" | grep -v grep | awk '{print $2}'`
if [[ -z "$vpid" && "$retval" -eq 0 ]]; then
    echo ":( , Failed, I can NOT kill $COMMAND running by $USER, got an error code $retval"
else 
    echo ":) , Successfully killed $COMMAND running by $USER"
fi