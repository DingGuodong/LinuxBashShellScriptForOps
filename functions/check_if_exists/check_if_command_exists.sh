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
  if [ -z "$(command -v "$@" 2> /dev/null)" ] || [ -z "$(command -v "$@" 2> /dev/null)" ] ; then
      return 1
  else
      return 0
  fi
}
