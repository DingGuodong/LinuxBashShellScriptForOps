#!/usr/bin/env bash
echo "create Swap which has same size of Memory"

free -b
DATA_PARTITION="/opt"
time dd if=/dev/zero of=$DATA_PARTITION/swap bs=512 count=$(($(free -b|awk '/Mem:/{print$2}') / 512))
chmod 600 $DATA_PARTITION/swap
mkswap $DATA_PARTITION/swap
sysctl -w vm.swappiness=10
swapon $DATA_PARTITION/swap
cp /etc/fstab /etc/fstab"$(date +%Y%m%d%H%M%S)"~
echo "$DATA_PARTITION/swap swap swap defaults    0  0" >> /etc/fstab
free -b
