#!/usr/bin/env bash
# Get the default routing IP
# get_default_host_ip
#校验验证IP是否合法
ipcalc -c  10.20.0.7

#egrep is the same as grep -E.
IP=$(ifconfig | grep inet | egrep -v "(inet6|127.0.0.1)" | awk -F ":" '{print $2}' | awk '{print $1}')
IP=$(ifconfig | grep inet | grep -Ev "(inet6|127.0.0.1)" | awk -F ":" '{print $2}' | awk '{print $1}')
hostname -i
facter ipaddress_eth0
# A system used standard method to get ip address from  '/etc/rc.d/rc.sysinit' line 346 on CentOS, useless for Ubuntu
ip addr show to 0.0.0.0/0 scope global | awk '/[[:space:]]inet / { print gensub("/.*","","g",$2) }'

# Ubuntu
DEVICE="`route -n | awk '/^0.0.0.0/ { print $NF  }'`"
ip addr show to 0.0.0.0/0 scope global $DEVICE | awk '/[[:space:]]inet / { print gensub("/.*","","g",$2) }'

# Get all IP
ifconfig | grep inet | egrep -v "(inet6|127.0.0.1)" | cut -d ":" -f2 | cut -d " " -f1

# CentOS IP
DEVICE=$(route -n | awk '/^0.0.0.0/ && /UG/ {print $NF}')
IP=$(ifconfig $DEVICE | awk -F '[ :]+' '/inet/ && !/inet6/ {print $3}')
echo $IP

# Ubuntu IP
DEVICE=$(route -n | awk '/^0.0.0.0/ && /UG/ {print $NF}')
IP=$(ifconfig $DEVICE | awk -F '[ :]+' '/inet/ && !/inet6/ {print $4}')
echo $IP

# general distro using ip command
ip addr show scope global $(ip route | awk '/^default/ {print $NF}') | awk -F '[ /]+' '/global/ {print $3}'

#without awk or cut
IP1=$(ifconfig | grep inet | egrep -v "(inet6|127.0.0.1)")
IP2=${IP1#*addr:}
IP=${IP2%% Bcast*}
echo $IP
