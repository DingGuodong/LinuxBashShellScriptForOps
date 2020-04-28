#!/usr/bin/env bash
# Get the default routing IP
# get_default_host_ip
#校验验证IP是否合法
ipcalc -c 10.20.0.7
# 验证一个IP是否是合法的IP需要与子网掩码一起计算
ipcalc -c 10.104.28.0/255.255.192.0

#egrep is the same as grep -E.
IP=$(ifconfig | grep inet | grep -Ev "(inet6|127.0.0.1)" | awk -F ":" '{print $2}' | awk '{print $1}')
hostname -i
facter ipaddress_eth0
# A system used standard method to get ip address from  '/etc/rc.d/rc.sysinit' line 346 on CentOS, useless for Ubuntu
ip addr show to 0.0.0.0/0 scope global | gawk '/[[:space:]]inet / { print gensub("/.*","","g",$2) }'

# Ubuntu
DEVICE="$(route -n | awk '/^0.0.0.0/ { print $NF  }')"
ip addr show to 0.0.0.0/0 scope global "${DEVICE}" | gawk '/[[:space:]]inet / { print gensub("/.*","","g",$2) }'

# Get all IP
ifconfig | grep inet | egrep -v "(inet6|127.0.0.1)" | cut -d ":" -f2 | cut -d " " -f1

# CentOS IP
DEVICE=$(route -n | awk '/^0.0.0.0/ && /UG/ {print $NF}')
IP=$(ifconfig "${DEVICE}" | awk -F '[ :]+' '/inet/ && !/inet6/ {print $3}')
echo "$IP"

# Ubuntu IP
DEVICE=$(route -n | awk '/^0.0.0.0/ && /UG/ {print $NF}')
IP=$(ifconfig "${DEVICE}" | awk -F '[ :]+' '/inet/ && !/inet6/ {print $4}')
echo "$IP"

# general distro using ip command
# TODO(Guodong Ding) Ubuntu 16.04.1 LTS maybe not support, see 'ip route' for detail
ip addr show scope global "$(ip route | awk '/^default/ {print $NF}')" | awk -F '[ /]+' '/global/ {print $3}'

#without awk or cut
IP1=$(ifconfig | grep inet | grep -Ev "(inet6|127.0.0.1)")
IP2=${IP1#*addr:}
IP=${IP2%% Bcast*}
echo "$IP"

# using grep
ifconfig | grep -Po '(?<=:).*(?=  B)'

# others
ifconfig eth0 | awk -F '[ :]+' 'NR==2 {print $4}'

# 获取内网网卡名称(适用于2个网卡，1个用做内网，1个用作外网), U (route is up), G (use gateway), see 'man route' Flags
route -n | awk '/UG/&&!/0.0.0.0/ {print$NF;exit}'

# 获取外网网卡名称
route -n | awk '/^0.0.0.0/ {print$NF}'

# 获取内网网卡IP地址(适用于2个网卡，1个用做内网，1个用作外网)
ip addr show scope global "$(route -n | awk '/UG/ && ! /0.0.0.0/ {print$NF;exit}')" | awk -F '[ /]+' '/global/ {print $3}'

# 获取外网网卡IP
ip addr show scope global "$(ip route | awk '/^default/ {print $5}')" | awk -F '[ /]+' '/global/ {print $3}'
