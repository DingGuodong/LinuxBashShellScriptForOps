#!/bin/bash
# Created by PyCharm.
# File Name:              LinuxBashShellScriptForOps:install_python27_centos6.sh
# Version:                0.0.1
# Author:                 Guodong
# Author Email:           dgdenterprise@gmail.com
# URL:                    https://github.com/DingGuodong/LinuxBashShellScriptForOps
# Download URL:           https://github.com/DingGuodong/LinuxBashShellScriptForOps/tarball/master
# Create Date:            2018/11/7
# Create Time:            16:35
# Description:            install python2.7 into CentOS 6.x
# Long Description:       
# Usage:                  
# References:             
# Prerequisites:          []
# Development Status:     3 - Alpha, 5 - Production/Stable
# Environment:            Console
# Intended Audience:      System Administrators, Developers, End Users/Desktop
# License:                Freeware, Freely Distributable
# Natural Language:       English, Chinese (Simplified)
# Operating System:       POSIX :: Linux
# Programming Language:   GNU bash :: 4+
# Topic:                  Utilities
set -e

PYTHON_VERSION=2.7.15  # current latest release version

python -V
ls -l `which python`
which python

v=`python -V |& grep -i py`
[[ ${v:7:3} == 2.7 ]] && echo "nothing need to do. now exit" && exit 0

test -f /usr/bin/yum~ || cp -f /usr/bin/yum /usr/bin/yum~
sed -i '1 s/python$/python2.6/g' /usr/bin/yum

wget -c https://www.python.org/ftp/python/${PYTHON_VERSION}/Python-${PYTHON_VERSION}.tgz
wget -c https://www.python.org/ftp/python/${PYTHON_VERSION}/Python-${PYTHON_VERSION}.tgz.asc
wget -c https://www.python.org/static/files/pubkeys.txt

gpg --import pubkeys.txt
gpg --recv-keys 6A45C816 36580288 7D9DC8D2 18ADD4FF A4135B38 A74B06BF EA5BBD71 ED9D77D5 E6DF025C AA65421D 6F5E1540 F73C700D 487034E5
gpg --verify Python-${PYTHON_VERSION}.tgz.asc

tar zxf Python-${PYTHON_VERSION}.tgz
cd Python-${PYTHON_VERSION}/
yum install -y gcc gcc-c++ openssl-devel
./configure --enable-shared
make && make install  # default installation path is '/usr/local'

echo '/usr/local/lib' > /etc/ld.so.conf.d/libpython2.7.conf
ldconfig

/usr/local/bin/python --version
ls /usr/local/bin/python*

wget -c https://bootstrap.pypa.io/ez_setup.py
/usr/local/bin/python ez_setup.py
/usr/local/bin/easy_install  --version
wget -c https://bootstrap.pypa.io/get-pip.py
/usr/local/bin/python get-pip.py
/usr/local/bin/pip --version

echo "ATTENTIONS: default python will not take effect unless user logout current session then login again"
echo "OK: finished."
set +e
