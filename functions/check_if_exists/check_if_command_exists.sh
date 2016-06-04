#!/usr/bin/env bash
# Check if a command already exists
function command_exists() {
    # which "$@" >/dev/null 2>&1
    command -v "$@" >/dev/null 2>&1
}

function command_exists_v2() {
    # man bash, search hash
    hash "$@" >/dev/null 2>&1
}

function is_command_exists(){
if [ -z "`which $@ 2> /dev/null`" -o -z "`which $* 2> /dev/null`" ] ; then
  # missing $@ and/or $*
  exit 0
fi
}