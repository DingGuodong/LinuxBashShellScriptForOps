#!/usr/bin/env bash
# Usage: bash $0
# Author: dgden
# Create Date: 2021/3/19
# Create Time: 14:10
# Description: allow the login ip access a port on this host

function remove_an_old_fw_rich_rule() {
  wanted_rich_rule=$(firewall-cmd --list-all | awk '/fw_temp_kw_phone/','$1=$1')
  if [[ $wanted_rich_rule != "" ]]; then
    firewall-cmd --permanent --zone=public --remove-rich-rule="$wanted_rich_rule"
    firewall-cmd --reload
  fi
}

function add_a_fw_rich_rule() {
  from_ip=$(bash -c "w -h | awk '/w -h/ {print \$3}'")
  firewall-cmd --permanent --add-rich-rule="rule family="ipv4" source address="$from_ip" port protocol="tcp" port="50009" log prefix="fw_temp_kw_phone" level="info" accept"
  firewall-cmd --reload
}

function main() {
  remove_an_old_fw_rich_rule
  add_a_fw_rich_rule
  firewall-cmd --list-all
}

main
