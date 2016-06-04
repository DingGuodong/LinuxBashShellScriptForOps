#!/bin/bash
stime=$(date +%s)
shstime=$(date +%H:%M:%S:%N)

sleep 2

etime=$(date +%s)
shetime=$(date +%H:%M:%S:%N)
shptime=$(expr ${etime} - ${stime})
echo ${shptime}