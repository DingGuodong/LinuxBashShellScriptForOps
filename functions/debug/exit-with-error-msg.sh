#!/usr/bin/env bash

function exit_with_error_msg() {
  msg="$1"    # message
  prefix="$2" # logger name
  lineno="$3" # line no

  echo "${prefix:="self"}: ${lineno:="undefined"}: ${msg:="default error msg"}."

  exit 1
}

echo "here"

# call example
exit_with_error_msg
exit_with_error_msg hello_message mylog $LINENO
