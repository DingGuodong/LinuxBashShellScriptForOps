#!/usr/bin/env bash
# Created by PyCharm.
# File:                 LinuxBashShellScriptForOps:yum_update_packages_safely.sh
# User:                 Guodong
# Create Date:          2017/8/11
# Create Time:          18:23
# Function:             
# Note:                 
# Prerequisite:         
# Description:          we can NOT use 'yum update -y' to update all packages on production environment,
# Reference:            


## yum repolist
#Loaded plugins: langpacks
#repo id                              repo name                                      status
#base/7/x86_64                        CentOS-7 - Base                                 9,363
#docker-main-repo                     Docker main Repository                            110
#epel/x86_64                          Extra Packages for Enterprise Linux 7 - x86_64 11,785
#extras/7/x86_64                      CentOS-7 - Extras                                 449
#gitlab-ce                            gitlab-ce                                         285
#gitlab_gitlab-ce/x86_64              gitlab_gitlab-ce                                  285
#gitlab_gitlab-ce-source              gitlab_gitlab-ce-source                             0
#runner_gitlab-ci-multi-runner/x86_64 runner_gitlab-ci-multi-runner                     101
#runner_gitlab-ci-multi-runner-source runner_gitlab-ci-multi-runner-source                0
#updates/7/x86_64                     CentOS-7 - Updates                              2,146
#repolist: 24,524


repo_list="`yum repolist | sed '1,3d;$d' | awk '{print $1}' | xargs | sed 's/\ /,/g'`"
packages_list="`yum check-update | sed '1,3d' | awk '{print $1}'| xargs`"

wanted_repo_list="base,epel,extras,updates"
unwanted_packages_list="gitlab-ce,gitlab-ci-multi-runner,docker-engine,docker-engine-selinux"

# TODO(Guodong Ding) NO QA
yum update --enablerepo=${wanted_repo_list} || yum update --exclude=${unwanted_packages_list}
