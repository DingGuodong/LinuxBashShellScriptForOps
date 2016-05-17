#!/usr/bin/env bash
# common date format
date +"%F-%H-%M-%S" # 2016-05-17-10-20-36
date +"%Y%m%d%H%M%S" # 20160517102021
date +"%Y/%m/%d %H:%M:%S %s" # 2016/05/17 10:20:07 1463451607
date +'%Y-%m-%d %H:%M:%S.%N %z' # 2016-05-17 10:19:54.070654194 +0800
date --rfc-2822 # equal to 'date -R', Tue, 17 May 2016 10:19:35 +0800
