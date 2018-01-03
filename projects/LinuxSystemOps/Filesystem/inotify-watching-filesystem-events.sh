#!/usr/bin/env bash
# Description:
# inotify-tools is a set of command-line programs for Linux providing
# a simple interface to inotify. These programs can be used to monitor
# and act upon filesystem events.

# References:
# https://www.infoq.com/articles/inotify-linux-file-system-event-monitoring

# Python version:
# [inotify 0.2.9](https://pypi.python.org/pypi/inotify)
# [inotifyx 0.2.2](https://pypi.python.org/pypi/inotifyx/0.2.2)
# [pyinotify 0.9.6](https://pypi.python.org/pypi/pyinotify/)

# Ubuntu, sudo apt install -y inotify-tools
# CentOS: epel, yum makecache; yum install -y epel-release; yum install -y inotify-tools

grep INOTIFY_USER /boot/config-$(uname -r) >/dev/null || exit 1
inotifywait --exclude '^/data/app/(large|ignore)/' -rme modify,attrib,move,close_write,create,delete,delete_self /data/app/

