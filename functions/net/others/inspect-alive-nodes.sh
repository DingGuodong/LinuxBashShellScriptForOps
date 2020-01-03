#!/usr/bin/env bash

# scan an IP
nmap -F 192.168.88.18 | grep 'Host is up'

# scan an IP using ping
nmap -n -sn 192.168.88.0/24

# scan a network
nmap -nF 192.168.88.0/24 | awk '/Nmap scan report for/ {print $NF}'

