#!/usr/bin/env bash
#
# Function description:
# determine which Linux distribution running
#
# Useful function list:
# is_centos
# is_ubuntu
# is_debian
# is_rhel
# is_package_installed "package" && install_package "package"
#
# Usage:
# <function-common> distro.sh
#
# Birth Time:
# 2016-04-28 18:04:27.151203523 +0800
#
# Author:
# Open Source Software written by 'Guodong Ding <dgdenterprise@gmail.com>'
# Blog: http://dgd2010.blog.51cto.com/
# Github: https://github.com/DingGuodong
#
# Refer:
# https://github.com/openstack-dev/devstack
# functions-common


# Save trace setting
_XTRACE_FUNCTIONS_COMMON=$(set +o | grep xtrace)
set +o xtrace

check_network_connectivity(){
    echo "checking network connectivity ... "
    network_address_to_check=8.8.4.4
    stable_network_address_to_check=114.114.114.114
    ping_count=2
    ping -c $ping_count $network_address_to_check >/dev/null
    retval=$?
    if [ $retval -ne 0 ] ; then
        if ping -c $ping_count $stable_network_address_to_check >/dev/null;then
            echo "Network to $stable_network_address_to_check succeed! "
            echo "Note: network to $network_address_to_check failed once! maybe just some packages loss."
        elif ! ip route | grep default >/dev/null; then
            echo "Network is unreachable, gateway is not set."
        elif ! ping -c2 $(ip route | awk '/default/ {print $3}') >/dev/null; then
            echo "Network is unreachable, gateway is unreachable."
        else
            echo "Network is blocked! "
            return 0
        fi
        OFFLINE="True"
        return 1
    elif [ $retval -eq 0 ]; then
        echo "Check network connectivity passed! "
        OFFLINE="False"
        return 0
    fi
}

check_name_resolve(){
    echo "checking DNS name resolve ... "
    target_name_to_resolve="github.com"
    stable_target_name_to_resolve="www.aliyun.com"
    ping_count=1
    if ! ping  -c$ping_count $target_name_to_resolve >/dev/null; then
        echo "Name lookup failed for $target_name_to_resolve with $ping_count times "
        if ping  -c$ping_count $stable_target_name_to_resolve >/dev/null; then
            echo "Name lookup success for $stable_target_name_to_resolve with $ping_count times "
        fi
        [ -f /etc/resolv.conf ] && cp /etc/resolv.conf /etc/resolv.conf_$(date +%Y%m%d%H%M%S)~
        cat >/etc/resolv.conf<<eof
nameserver 8.8.4.4
nameserver 114.114.114.114
eof
    check_name_resolve
    else
        echo "Check DNS name resolve passed! "
        return 0
    fi

}

# Like sudo but forwarding http_proxy https_proxy no_proxy environment vars.
# If it is run as superuser then sudo is replaced by env.
#
function sudo_with_proxies() {
    local sudo

    [[ "$(id -u)" = "0" ]] && sudo="env" || sudo="sudo"

    $sudo http_proxy="${http_proxy:-}" https_proxy="${https_proxy:-}"\
        no_proxy="${no_proxy:-}" "$@"
}


# Timing infrastructure - figure out where large blocks of time are
# used
#
# The timing infrastructure is about collecting buckets
# of time that are spend in some sub-task. For instance, that might be
# 'apt', 'pip', 'osc', even database migrations. We do this by a pair
# of functions: time_start / time_stop.
#
# These take a single parameter: $name - which specifies the name of
# the bucket to be accounted against. time_totals function spits out
# the results.
#
# Resolution is only in whole seconds, so should be used for long
# running activities.

declare -A _TIME_TOTAL=()
declare -A _TIME_START=()
declare -r _TIME_BEGIN=$(date +%s)

# time_start $name
#
# starts the clock for a timer by name. Errors if that clock is
# already started.
function time_start() {
    local name=$1
    local start_time=${_TIME_START[$name]}
    if [[ -n "$start_time" ]]; then
        die $LINENO "Trying to start the clock on $name, but it's already been started"
    fi
    _TIME_START[$name]=$(date +%s)
}

# time_stop $name
#
# stops the clock for a timer by name, and accumulate that time in the
# global counter for that name. Errors if that clock had not
# previously been started.
function time_stop() {
    local name
    local end_time
    local elapsed_time
    local total
    local start_time

    name=$1
    start_time=${_TIME_START[$name]}

    if [[ -z "$start_time" ]]; then
        die $LINENO "Trying to stop the clock on $name, but it was never started"
    fi
    end_time=$(date +%s)
    elapsed_time=$(($end_time - $start_time))
    total=${_TIME_TOTAL[$name]:-0}
    # reset the clock so we can start it in the future
    _TIME_START[$name]=""
    _TIME_TOTAL[$name]=$(($total + $elapsed_time))
}

# time_totals
#  Print out total time summary
function time_totals() {
    local elapsed_time
    local end_time
    local len=15
    local xtrace

    end_time=$(date +%s)
    elapsed_time=$(($end_time - $_TIME_BEGIN))

    # pad 1st column this far
    t=()
    for t in ${!_TIME_TOTAL[*]}; do
        if [[ ${#t} -gt $len ]]; then
            len=${#t}
        fi
    done

    xtrace=$(set +o | grep xtrace)
    set +o xtrace

    echo
    printf "%-${len}s %3d\n" "Total runtime" "$elapsed_time"
    echo
    t=()
    for t in ${!_TIME_TOTAL[*]}; do
        local v=${_TIME_TOTAL[$t]}
        printf "%-${len}s %3d\n" "$t" "$v"
    done

    $xtrace
}


# Prints backtrace info
# backtrace level
function backtrace() {
    local level=$1
    local deep
    deep=$((${#BASH_SOURCE[@]} - 1))
    echo "[Call Trace]"
    while [ $level -le $deep ]; do
        echo "${BASH_SOURCE[$deep]}:${BASH_LINENO[$deep-1]}:${FUNCNAME[$deep-1]}"
        deep=$((deep - 1))
    done
}

# Prints line number and "message" in error format
# err $LINENO "message"
function err() {
    local exitcode=$?
    local xtrace
    xtrace=$(set +o | grep xtrace)
    set +o xtrace
    local msg="[ERROR] ${BASH_SOURCE[2]}:$1 $2"
    echo $msg 1>&2;
    if test -n ${LOGDIR}; then
        echo $msg >> "${LOGDIR}/error.log"
    fi
    $xtrace
    return $exitcode
}

# Checks an environment variable is not set or has length 0 OR if the
# exit code is non-zero and prints "message"
# NOTE: env-var is the variable name without a '$'
# err_if_not_set $LINENO env-var "message"
function err_if_not_set() {
    local exitcode=$?
    local xtrace
    xtrace=$(set +o | grep xtrace)
    set +o xtrace
    local line=$1; shift
    local val=$1; shift
    if ! is_set $val || [ $exitcode != 0 ]; then
        err $line "$*"
    fi
    $xtrace
    return $exitcode
}

# Test if the named environment variable is set and not zero length
# is_set env-var
function is_set() {
    local var=\$"$1"
    eval "[ -n \"$var\" ]" # For ex.: sh -c "[ -n \"$var\" ]" would be better, but several exercises depends on this
}

# Prints line number and "message" then exits
# die $LINENO "message"
# $LINENO is refer to "man bash": BASH_LINENO, Use LINENO to obtain the current line number.
function die() {
    local exitcode=$?
    set +o xtrace
    local line=$1; shift
    if [ $exitcode == 0 ]; then
        exitcode=1
    fi
    backtrace 2
    err $line "$*"
    # Give buffers a second to flush
    sleep 1
    exit $exitcode
}

# Checks an environment variable is not set or has length 0 OR if the
# exit code is non-zero and prints "message" and exits
# NOTE: env-var is the variable name without a '$'
# die_if_not_set $LINENO env-var "message"
function die_if_not_set() {
    local exitcode=$?
    local xtrace
    xtrace=$(set +o | grep xtrace)
    set +o xtrace
    local line=$1; shift
    local val=$1; shift
    if ! is_set $val || [ $exitcode != 0 ]; then
        die $line "$*"
    fi
    $xtrace
}

function deprecated() {
    local text=$1
    DEPRECATED_TEXT+="\n$text"
    echo "WARNING: $text"
}

# Prints line number and "message" in warning format
# warn $LINENO "message"
function warn() {
    local exitcode=$?
    local xtrace
    xtrace=$(set +o | grep xtrace)
    set +o xtrace
    local msg="[WARNING] ${BASH_SOURCE[2]}:$1 $2"
    echo $msg
    $xtrace
    return $exitcode
}

# Distro Functions
# ================

# Determine OS Vendor, Release and Update

#
# NOTE : For portability, you almost certainly do not want to use
# these variables directly!  The "is_*" functions defined below this
# bundle up compatible platforms under larger umbrellas that we have
# determined are compatible enough (e.g. is_ubuntu covers Ubuntu &
# Debian, is_fedora covers RPM-based distros).  Higher-level functions
# such as "install_package" further abstract things in better ways.
#
# ``OS_VENDOR`` - vendor name: ``Ubuntu``, ``Fedora``, etc
# ``OS_RELEASE`` - major release: ``14.04`` (Ubuntu), ``20`` (Fedora)
# ``OS_PACKAGE`` - package type: ``deb`` or ``rpm``
# ``OS_CODENAME`` - vendor's codename for release: ``trusty``

declare OS_VENDOR OS_RELEASE OS_PACKAGE OS_CODENAME

# Make a *best effort* attempt to install lsb_release packages for the
# user if not available.  Note can't use generic install_package*
# because they depend on this!
function _ensure_lsb_release(){
    if test -x $(command -v lsb_release 2>/dev/null); then
        return
    fi
    if test -x $(command -v apt-get 2>/dev/null); then
        sudo apt-get install -y lsb-release
    elif test -x $(command -v zypper 2>/dev/null); then
        # XXX: old code paths seem to have assumed SUSE platforms also
        # had "yum".  Keep this ordered above yum so we don't try to
        # install the rh package.  suse calls it just "lsb"
        sudo zypper -n install lsb
    elif test -x $(command -v dnf 2>/dev/null); then
        sudo dnf install -y redhat-lsb-core
    elif test -x $(command -v yum 2>/dev/null); then
        # all rh platforms (fedora, centos, rhel) have this pkg
        sudo yum install -y redhat-lsb-core
    else
        die $LINENO "Unable to find or auto-install lsb_release"
    fi
}

# GetOSVersion
#  Set the following variables:
#  - OS_RELEASE
#  - OS_CODENAME
#  - OS_VENDOR
#  - OS_PACKAGE
function GetOSVersion(){
    # We only support distros that provide a sane lsb_release
    _ensure_lsb_release

    OS_RELEASE=$(lsb_release -r -s)
    OS_CODENAME=$(lsb_release -c -s)
    OS_VENDOR=$(lsb_release -i -s)
    if [[ ${OS_VENDOR} =~ (Debian|Ubuntu|LinuxMint) ]]; then
        OS_PACKAGE="deb"
    else
        OS_PACKAGE="rpm"
    fi

    typeset -xr OS_VENDOR
    typeset -xr OS_RELEASE
    typeset -xr OS_PACKAGE
    typeset -xr OS_CODENAME
}

# Translate the OS version values into common nomenclature
# Sets global ``DISTRO`` from the ``os_*`` values
declare DISTRO

function GetDistro() {
    GetOSVersion
    if [[ "$OS_VENDOR" =~ (Ubuntu) || "$OS_VENDOR" =~ (Debian) || \
            "$OS_VENDOR" =~ (LinuxMint) ]]; then
        # 'Everyone' refers to Ubuntu / Debian / Mint releases by
        # the code name adjective
        DISTRO=$OS_CODENAME
    elif [[ "$OS_VENDOR" =~ (Fedora) ]]; then
        # For Fedora, just use 'f' and the release
        DISTRO="f$OS_RELEASE"
    elif [[ "$OS_VENDOR" =~ (openSUSE) ]]; then
        DISTRO="opensuse-$OS_RELEASE"
    elif [[ "$OS_VENDOR" =~ (SUSE LINUX) ]]; then
        # just use major release
        DISTRO="sle${OS_RELEASE%.*}"
    elif [[ "$OS_VENDOR" =~ (Red.*Hat) || \
        "$OS_VENDOR" =~ (CentOS) || \
        "$OS_VENDOR" =~ (OracleServer) || \
        "$OS_VENDOR" =~ (Virtuozzo) ]]; then
        # Drop the . release as we assume it's compatible
        # XXX re-evaluate when we get RHEL10
        DISTRO="rhel${OS_RELEASE::1}"
    elif [[ "$OS_VENDOR" =~ (XenServer) ]]; then
        DISTRO="xs${OS_RELEASE%.*}"
    elif [[ "$OS_VENDOR" =~ (kvmibm) ]]; then
        DISTRO="${OS_VENDOR}${OS_RELEASE::1}"
    else
        # We can't make a good choice here.  Setting a sensible DISTRO
        # is part of the problem, but not the major issue -- we really
        # only use DISTRO in the code as a fine-filter.
        #
        # The bigger problem is categorising the system into one of
        # our two big categories as Ubuntu/Debian-ish or
        # Fedora/CentOS-ish.
        #
        # The setting of OS_PACKAGE above is only set to "deb" based
        # on a hard-coded list of vendor names ... thus we will
        # default to thinking unknown distros are RPM based
        # (ie. is_ubuntu does not match).  But the platform will then
        # also not match in is_fedora, because that also has a list of
        # names.
        #
        # So, if you are reading this, getting your distro supported
        # is really about making sure it matches correctly in these
        # functions.  Then you can choose a sensible way to construct
        # DISTRO based on your distros release approach.
        die $LINENO "Unable to determine DISTRO, can not continue."
    fi
    typeset -xr DISTRO
}

# Utility function for checking machine architecture
# is_arch arch-type
function is_arch() {
    [[ "$(uname -m)" == "$1" ]]
}

# Determine if current distribution is an Oracle distribution
# is_oraclelinux
function is_oraclelinux() {
    if [[ -z "$OS_VENDOR" ]]; then
        GetOSVersion
    fi

    [ "$OS_VENDOR" = "OracleServer" ]
}


# Determine if current distribution is a Fedora-based distribution
# (Fedora, RHEL, CentOS, etc).
# is_fedora
function is_fedora() {
    if [[ -z "$OS_VENDOR" ]]; then
        GetOSVersion
    fi

    [ "$OS_VENDOR" = "Fedora" ] || [ "$OS_VENDOR" = "Red Hat" ] || \
        [ "$OS_VENDOR" = "RedHatEnterpriseServer" ] || \
        [ "$OS_VENDOR" = "CentOS" ] || [ "$OS_VENDOR" = "OracleServer" ] || \
        [ "$OS_VENDOR" = "Virtuozzo" ]
}

# Determine if current distribution is a Fedora-based distribution
# (Fedora, RHEL, CentOS, etc).
# is_centos
function is_centos() {
    if [[ -z "$OS_VENDOR" ]]; then
        GetOSVersion
    fi

    [ "$OS_VENDOR" = "Fedora" ] || [ "$OS_VENDOR" = "Red Hat" ] || \
        [ "$OS_VENDOR" = "RedHatEnterpriseServer" ] || \
        [ "$OS_VENDOR" = "CentOS" ] || [ "$OS_VENDOR" = "OracleServer" ] || \
        [ "$OS_VENDOR" = "Virtuozzo" ]
}

# Determine if current distribution is a Fedora-based distribution
# (Fedora, RHEL, CentOS, etc).
# is_rhel
function is_rhel() {
    if [[ -z "$OS_VENDOR" ]]; then
        GetOSVersion
    fi

    [ "$OS_VENDOR" = "Fedora" ] || [ "$OS_VENDOR" = "Red Hat" ] || \
        [ "$OS_VENDOR" = "RedHatEnterpriseServer" ] || \
        [ "$OS_VENDOR" = "CentOS" ] || [ "$OS_VENDOR" = "OracleServer" ] || \
        [ "$OS_VENDOR" = "Virtuozzo" ]
}

# Determine if current distribution is a SUSE-based distribution
# (openSUSE, SLE).
# is_suse
function is_suse() {
    if [[ -z "$OS_VENDOR" ]]; then
        GetOSVersion
    fi

    [[ "$OS_VENDOR" =~ (openSUSE) || "$OS_VENDOR" == "SUSE LINUX" ]]
}


# Determine if current distribution is an Ubuntu-based distribution
# It will also detect non-Ubuntu but Debian-based distros
# is_ubuntu
function is_ubuntu() {
    if [[ -z "$OS_PACKAGE" ]]; then
        GetOSVersion
    fi
    [ "$OS_PACKAGE" = "deb" ]
}

# Determine if current distribution is an Ubuntu-based distribution
# It will also detect non-Ubuntu but Debian-based distros
# is_debian
function is_debian() {
    if [[ -z "$OS_PACKAGE" ]]; then
        GetOSVersion
    fi
    [ "$OS_PACKAGE" = "deb" ]
}


# Exit after outputting a message about the distribution not being supported.
# exit_distro_not_supported [optional-string-telling-what-is-missing]
function exit_distro_not_supported() {
    if [[ -z "$DISTRO" ]]; then
        GetDistro
    fi

    if [ $# -gt 0 ]; then
        die $LINENO "Support for $DISTRO is incomplete: no support for $@"
    else
        die $LINENO "Support for $DISTRO is incomplete."
    fi
}

# Wrapper for ``apt-get update`` to try multiple times on the update
# to address bad package mirrors (which happen all the time).
function apt_get_update() {
    # only do this once per run
    if [[ "$REPOS_UPDATED" == "True" && "$RETRY_UPDATE" != "True" ]]; then
        return
    fi

    # bail if we are offline
    check_network_connectivity
    [[ "$OFFLINE" = "True" ]] && return

    local sudo="sudo"
    [[ "$(id -u)" = "0" ]] && sudo="env"

    # time all the apt operations
    time_start "apt-get-update"

    local proxies="http_proxy=${http_proxy:-} https_proxy=${https_proxy:-} no_proxy=${no_proxy:-} "
    local update_cmd="$sudo $proxies apt-get update"
    if ! timeout 300 sh -c "while ! $update_cmd; do sleep 30; done"; then
        die $LINENO "Failed to update apt repos, we're dead now"
    fi

    REPOS_UPDATED=True
    # stop the clock
    time_stop "apt-get-update"
}

# Wrapper for ``apt-get`` to set cache and proxy environment variables
# Uses globals ``OFFLINE``, ``*_proxy``
# apt_get operation package [package ...]
function apt_get() {
    local xtrace result
    xtrace=$(set +o | grep xtrace)
    set +o xtrace

    check_network_connectivity
    [[ "$OFFLINE" = "True" || -z "$@" ]] && return
    local sudo="sudo"
    [[ "$(id -u)" = "0" ]] && sudo="env"

    # time all the apt operations
    time_start "apt-get"

    $xtrace

    $sudo DEBIAN_FRONTEND=noninteractive \
        http_proxy=${http_proxy:-} https_proxy=${https_proxy:-} \
        no_proxy=${no_proxy:-} \
        apt-get --option "Dpkg::Options::=--force-confold" --assume-yes "$@" < /dev/null
    result=$?

    # stop the clock
    time_stop "apt-get"
    return $result
}

# Distro-agnostic package installer
# Uses globals ``NO_UPDATE_REPOS``, ``REPOS_UPDATED``, ``RETRY_UPDATE``
# install_package package [package ...]
function update_package_repo() {
    NO_UPDATE_REPOS=${NO_UPDATE_REPOS:-False}
    REPOS_UPDATED=${REPOS_UPDATED:-False}
    RETRY_UPDATE=${RETRY_UPDATE:-False}

    if [[ "$NO_UPDATE_REPOS" = "True" ]]; then
        return 0
    fi

    if is_ubuntu; then
        apt_get_update
    fi
}

function real_install_package() {
    if is_ubuntu; then
        apt_get install "$@"
    elif is_fedora; then
        yum_install "$@"
    elif is_suse; then
        zypper_install "$@"
    else
        exit_distro_not_supported "installing packages"
    fi
}

# Distro-agnostic package installer
# install_package package [package ...]
function install_package() {
    update_package_repo
    if ! real_install_package "$@"; then
        RETRY_UPDATE=True update_package_repo && real_install_package "$@"
    fi
}

# Distro-agnostic function to tell if a package is installed
# is_package_installed package [package ...]
function is_package_installed() {
    if [[ -z "$@" ]]; then
        return 1
    fi

    if [[ -z "$OS_PACKAGE" ]]; then
        GetOSVersion
    fi

    if [[ "$OS_PACKAGE" = "deb" ]]; then
        dpkg -s "$@" > /dev/null 2> /dev/null
    elif [[ "$OS_PACKAGE" = "rpm" ]]; then
        rpm --quiet -q "$@"
    else
        exit_distro_not_supported "finding if a package is installed"
    fi
}

# Distro-agnostic package uninstaller
# uninstall_package package [package ...]
function uninstall_package() {
    if is_ubuntu; then
        apt_get purge "$@"
    elif is_fedora; then
        sudo ${YUM:-yum} remove -y "$@" ||:
    elif is_suse; then
        sudo zypper rm "$@" ||:
    else
        exit_distro_not_supported "uninstalling packages"
    fi
}

# Wrapper for ``yum`` to set proxy environment variables
# Uses globals ``OFFLINE``, ``*_proxy``, ``YUM``
# yum_install package [package ...]
function yum_install() {
    local result parse_yum_result

    check_network_connectivity
    [[ "$OFFLINE" = "True" ]] && return

    time_start "yum_install"

    # - We run with LC_ALL=C so string matching *should* be OK
    # - Exit 1 if the failure might get better with a retry.
    # - Exit 2 if it is fatal.
    parse_yum_result='             \
        BEGIN { result=0 }         \
        /^YUM_FAILED/ { exit $2 }  \
        /^No package/ { result=2 } \
        /^Failed:/    { result=2 } \
        //{ print }                \
        END { exit result }'

    # The manual check for missing packages is because yum -y assumes
    # missing or failed packages are OK.
    # See https://bugzilla.redhat.com/show_bug.cgi?id=965567
    (sudo_with_proxies "${YUM:-yum}" install -y "$@" 2>&1 || echo YUM_FAILED $?) \
        | awk "$parse_yum_result" && result=$? || result=$?

    time_stop "yum_install"

    # if we return 1, then the wrapper functions will run an update
    # and try installing the package again as a defense against bad
    # mirrors.  This can hide failures, especially when we have
    # packages that are in the "Failed:" section because their rpm
    # install scripts failed to run correctly (in this case, the
    # package looks installed, so when the retry happens we just think
    # the package is OK, and incorrectly continue on).
    if [ "$result" == 2 ]; then
        die "Detected fatal package install failure"
    fi

    return "$result"
}

# zypper wrapper to set arguments correctly
# Uses globals ``OFFLINE``, ``*_proxy``
# zypper_install package [package ...]
function zypper_install() {
    check_network_connectivity
    [[ "$OFFLINE" = "True" ]] && return
    local sudo="sudo"
    [[ "$(id -u)" = "0" ]] && sudo="env"
    $sudo http_proxy="${http_proxy:-}" https_proxy="${https_proxy:-}" \
        no_proxy="${no_proxy:-}" \
        zypper --non-interactive install --auto-agree-with-licenses "$@"
}


# Restore xtrace
$_XTRACE_FUNCTIONS_COMMON
