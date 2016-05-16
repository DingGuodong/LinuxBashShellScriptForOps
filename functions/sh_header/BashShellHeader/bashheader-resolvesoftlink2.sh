#!/bin/bash

# resolve links - $0 may be a symbolic link

# learning from ActiveMQ
# get a canonical path, macosx and slowlaris does not support readlink -f :-)
pathCanonical() {
    local dst="${1}"
    while [ -h "${dst}" ] ; do
        ls=`ls -ld "${dst}"`
        link=`expr "$ls" : '.*-> \(.*\)$'`
        if expr "$link" : '/.*' > /dev/null; then
            dst="$link"
        else
            dst="`dirname "${dst}"`/$link"
        fi
    done
    local bas="`basename "${dst}"`"
    local dir="`dirname "${dst}"`"
    if [ "$bas" != "$dir" ]; then
      dst="`pathCanonical "$dir"`/$bas"
    fi
    echo "${dst}" | sed -e 's#//#/#g' -e 's#/\./#/#g' -e 's#/[^/]*/\.\./#/#g'
}

# a simple helper to get the activemq installation dir
getActiveMQHome(){
  # get the real path to the binary
  local REAL_BIN="`pathCanonical $0`"
  local REAL_DIR="`dirname $REAL_BIN`/../"
  REAL_DIR="`cd $REAL_DIR && pwd -P`"
  if [ -z "$REAL_DIR" ];then
      echo 'ERROR: unable to find real installation path fo activemq, you have to define ACTIVEMQ_HOME manually in the config' >&2
      exit 1
  fi
  echo "$REAL_DIR/"

}

# Active MQ installation dir
if [ -z "$ACTIVEMQ_HOME" ] ; then
  ACTIVEMQ_HOME="`getActiveMQHome`"
fi

