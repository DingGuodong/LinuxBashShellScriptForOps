#!/usr/bin/env bash
# Usage: sudo bash $0
# Author: dgden
# Create Date: 2020/9/23
# Create Time: 10:00
# Description: disable some motd scripts to improve login performance

[ -r /etc/os-release ] && . /etc/os-release

if [[ $ID != "ubuntu" ]]; then
  echo "for Debian dist like use only."
  exit 2
fi

printf "Welcome to %s (%s %s %s)\n" "$VERSION" "$(uname -o)" "$(uname -r)" "$(uname -m)"

chmod -x /etc/update-motd.d/10-help-text
chmod -x /etc/update-motd.d/50-motd-news
chmod -x /etc/update-motd.d/95-hwe-eol
