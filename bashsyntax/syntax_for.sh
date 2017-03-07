#!/usr/bin/env bash
#!/bin/bash
for (( i=1 ; i<5 ; i++ )); do echo ${i};done

a=(1 2 3); for i in ${!a[@]}; do echo ${a[i]}; done

ping_ip(){
    # Fixed TODO(Guodong Ding) pycharm Evaluate expansion Replace a bash expansion with the evaluated result
    # for i in {120..125}; do
    for i in $(seq 120 125); do
        if ping -c 1 -W 1 192.168.100.${i} &>/dev/null; then
            echo "192.168.100.$i is up"
        else
            echo "192.168.100.$i is down"
        fi
    done
}
ping_ip
