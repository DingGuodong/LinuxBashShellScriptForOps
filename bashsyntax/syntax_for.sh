#!/usr/bin/env bash
for (( i=1 ; i<5 ; i++ )); do echo ${i};done

a=(1 2 3); for i in ${!a[@]}; do echo ${a[i]}; done
