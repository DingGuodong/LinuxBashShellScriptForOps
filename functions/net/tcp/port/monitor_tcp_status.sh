#!/usr/bin/env bash
# code snippets for TCP status monitoring

tcp_summary_statistics=$(ss -s)

function get_tcp_state_from_ss() {
  case $1 in
  tcp_total | total)
    echo "$tcp_summary_statistics" | awk "NR==2" | awk '{print $2}'
    ;;
  tcp_estab | estab)
    echo "$tcp_summary_statistics" | awk "NR==2" | awk '{print +$4}'
    ;;
  tcp_closed | closed)
    echo "$tcp_summary_statistics" | awk "NR==2" | awk '{print +$6}'
    ;;
  tcp_orphaned | orphaned)
    echo "$tcp_summary_statistics" | awk "NR==2" | awk '{print +$8}'
    ;;
  tcp_synrecv | synrecv)
    echo "$tcp_summary_statistics" | awk "NR==2" | awk '{print +$10}'
    ;;
  tcp_timewait | timewait)
    echo "$tcp_summary_statistics" | awk "NR==2" | awk '{print +$12}'
    ;;
  tcp_ports | ports)
    echo "$tcp_summary_statistics" | awk "NR==2" | awk '{print +$NF}'
    ;;
  esac
}

function get_tcp_states_from_netstat() {
  #  netstat -n | awk '/^tcp/ {++STATES[$NF]} END {for(TYPE in STATES) print TYPE, STATES[TYPE]}'
  #  netstat -n | awk '/^tcp/ {++STATES[$NF]} END {print STATES["TIME_WAIT"]}'
  netstat -n | awk "/^tcp/ {++STATES[\$NF]} END {print STATES[\"$1\"]}"
}


get_tcp_state_from_ss total
get_tcp_state_from_ss estab
get_tcp_state_from_ss closed
get_tcp_state_from_ss orphaned
get_tcp_state_from_ss synrecv
get_tcp_state_from_ss timewait
get_tcp_state_from_ss ports


get_tcp_states_from_netstat TIME_WAIT
get_tcp_states_from_netstat SYN_SENT
get_tcp_states_from_netstat FIN_WAIT1
get_tcp_states_from_netstat FIN_WAIT2
get_tcp_states_from_netstat ESTABLISHED
get_tcp_states_from_netstat CLOSING
