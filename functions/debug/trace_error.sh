#!/usr/bin/env bash
# Print the commands being run so that we can see the command that triggers
# an error.  It is also useful for following along as the install occurs.
# same as set -u
# Save trace setting

# debug option
DEBUG=false
#DEBUG=true

if ${DEBUG} ; then
    old_PS4=$PS4
#    export PS4='+${BASH_SOURCE}:${LINENO}:${FUNCNAME[0]}: '
    export PS4='+${LINENO}: ${FUNCNAME[0]}: ' # if there is only one bash script, do not display ${BASH_SOURCE}
    _XTRACE_FUNCTIONS=$(set +o | grep xtrace)
    set -o xtrace
fi

###############################
# do something you want here
###############################
# debug option
if ${DEBUG} ; then
    export PS4=${old_PS4}
    ${_XTRACE_FUNCTIONS}
fi
