#!/usr/bin/env bash
# Usage: bash $0
# Author: dgden
# Create Date: 2020/9/14
# Create Time: 15:41
# Description: using sudo without input password

if [[ "$USER" == "root" ]]; then
  echo "FATAL ERROR: do NOT use root or sudo to execute $0"
  exit 1
else
  # https://www.quora.com/Who-wrote-the-message-that-comes-up-when-you-use-sudo-for-the-first-time
  echo "
\"\"\"
  We trust you have received the usual lecture from the local System
Administrator. It usually boils down to these three things:

    #1) Respect the privacy of others.
    #2) Think before you type.
    #3) With great power comes great responsibility.
\"\"\"
  "

fi

sudo tee /etc/sudoers.d/"$USER" <<eof
$USER ALL=(ALL) NOPASSWD: ALL
eof

sudo visudo -cf /etc/sudoers.d/"$USER"
