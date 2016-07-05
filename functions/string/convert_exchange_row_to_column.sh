#!/usr/bin/env bash
original_ip_list="`w -h | awk '/[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}/ {print $3}'`"
# Linux bash convert string from row to column?
echo "$original_ip_list" | tr ' ' '\n'
# how to convert rows into column using awk?
echo "$original_ip_list" | awk '{printf("%s ", $0)}'
echo "$original_ip_list" | tr'\n' ' '
echo "$original_ip_list" | xargs -n1