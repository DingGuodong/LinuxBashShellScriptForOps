#!/bin/bash
if [ "$(id -u)" != "0" ]; then
   echo "This script must be run as root" 1>&2
   exit 1
fi

DISTRO=
OS=

if grep 'Debian' /etc/issue > /dev/null 2>&1 ; then
    OS=debian
    DISTRO=debian
fi

if grep 'Ubuntu' /etc/issue > /dev/null 2>&1 ; then
    OS=debian
    DISTRO=ubuntu
fi

if grep 'ubuntu' /etc/os-release > /dev/null 2>&1 ; then
    OS=debian
    DISTRO=ubuntu
fi

if grep 'CentOS' /etc/issue > /dev/null 2>&1 ; then
    OS=rhel
    DISTRO=centos
fi

if grep 'CentOS' /etc/os-release > /dev/null 2>&1 ; then
    OS=rhel
    DISTRO=centos
fi

if grep 'Red' /etc/issue > /dev/null 2>&1 ; then
    OS=rhel
    DISTRO=rhel
fi

if [ ! ${OS} ] ; then
    echo ":: Could not detect OS"
    echo ":: Press Enter to continue"
    read -n1
fi


echo ":: OS: $OS"
echo ":: Distro: $DISTRO"

if [ "$OS" == "rhel" ] ; then
    echo
fi

if [ "$OS" == "debian" ] ; then
    echo
fi
