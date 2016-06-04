#!/usr/bin/env bash
# Control Functions
# =================

# Prints backtrace info
# filename:lineno:function
# backtrace level
function backtrace {
    local level=$1
    local deep
    deep=$((${#BASH_SOURCE[@]} - 1))
    echo "[Call Trace]"
    while [ ${level} -le ${deep} ]; do
        echo "${BASH_SOURCE[$deep]}:${BASH_LINENO[$deep-1]}:${FUNCNAME[$deep-1]}"
        deep=$((deep - 1))
    done
}

# Prints line number and "message" then exits
# die $LINENO "message"
function die {
    local exitcode=$?
    set +o xtrace
    local line=$1; shift
    if [ ${exitcode} == 0 ]; then
        exitcode=1
    fi
    backtrace 2
    err ${line} "$*"
    # Give buffers a second to flush
    sleep 1
    exit ${exitcode}
}

# Checks an environment variable is not set or has length 0 OR if the
# exit code is non-zero and prints "message" and exits
# NOTE: env-var is the variable name without a '$'
# die_if_not_set $LINENO env-var "message"
function die_if_not_set {
    local exitcode=$?
    local xtrace
    xtrace=$(set +o | grep xtrace)
    set +o xtrace
    local line=$1; shift
    local evar=$1; shift
    if ! is_set ${evar} || [ ${exitcode} != 0 ]; then
        die ${line} "$*"
    fi
    ${xtrace}
}

function deprecated {
    local text=$1
    DEPRECATED_TEXT+="\n$text"
    echo "WARNING: $text"
}

# Prints line number and "message" in error format
# err $LINENO "message"
function err {
    local exitcode=$?
    local xtrace
    xtrace=$(set +o | grep xtrace)
    set +o xtrace
    local msg="[ERROR] ${BASH_SOURCE[2]}:$1 $2"
    echo ${msg} 1>&2;
    if [[ -n ${LOGDIR} ]]; then
        echo "$msg" >> "${LOGDIR}/error.log"
    fi
    ${xtrace}
    return ${exitcode}
}

# Checks an environment variable is not set or has length 0 OR if the
# exit code is non-zero and prints "message"
# NOTE: env-var is the variable name without a '$'
# err_if_not_set $LINENO env-var "message"
function err_if_not_set {
    local exitcode=$?
    local xtrace
    xtrace=$(set +o | grep xtrace)
    set +o xtrace
    local line=$1; shift
    local evar=$1; shift
    if ! is_set ${evar} || [ ${exitcode} != 0 ]; then
        err ${line} "$*"
    fi
    ${xtrace}
    return ${exitcode}
}

# Test if the named environment variable is set and not zero length
# is_set env-var
function is_set {
    local var=\$"$1"
    eval "[ -n \"${var}\" ]" # For ex.: sh -c "[ -n \"$var\" ]" would be better, but several exercises depends on this
}

# Prints line number and "message" in warning format
# warn $LINENO "message"
function warn {
    local exitcode=$?
    local xtrace
    xtrace=$(set +o | grep xtrace)
    set +o xtrace
    local msg="[WARNING] ${BASH_SOURCE[2]}:$1 $2"
    echo ${msg}
    ${xtrace}
    return ${exitcode}
}
