#!/bin/sh
# From-release: CentOS release 6.8 (Final)
# From-file: /lib/lsb/init-functions

# LSB initscript functions, as defined in the LSB Spec 1.1.0
#
# Lawrence Lim <llim@redhat.com> - Tue, 26 June 2007
# Updated to the latest LSB 3.1 spec
# http://refspecs.freestandards.org/LSB_3.1.0/LSB-Core-generic/LSB-Core-generic_lines.txt

start_daemon () {
    /etc/redhat-lsb/lsb_start_daemon "$@"
}

killproc () {
    /etc/redhat-lsb/lsb_killproc "$@"
}

pidofproc () {
    /etc/redhat-lsb/lsb_pidofproc "$@"
}

log_success_msg () {
    /etc/redhat-lsb/lsb_log_message success "$@"
}

log_failure_msg () {
    /etc/redhat-lsb/lsb_log_message failure "$@"
}

log_warning_msg () {
    /etc/redhat-lsb/lsb_log_message warning "$@"
}
