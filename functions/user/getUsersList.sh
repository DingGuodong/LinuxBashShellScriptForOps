#!/usr/bin/env bash
# Refers: man useradd
UID_MAX=6000
UID_MIN=1000
SYS_UID_MAX=$((UID_MIN - 1))
SYS_UID_MIN=101

# root user
awk -F":" '$3==0 {print}' /etc/passwd

# system user
awk -F":" "\$3>=$SYS_UID_MIN&&\$3<$SYS_UID_MAX{print}" /etc/passwd

# normal user
awk -F":" "\$3>=$UID_MIN&&\$3<$UID_MAX {print}" /etc/passwd
