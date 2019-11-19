#!/usr/bin/env bash
# code snippets for SSH security enhancement

# deprecated
function check_and_set_for_nonroots() {
  find /home -name authorized_keys -type f -print0 | xargs -i chmod 400 {}
  find /home -name .ssh -type d -print0 | xargs -i chmod 500 {}
}

function check_and_set_for_common_users() {
  awk -F: '{if($3>500)print$6}' /etc/passwd | while IFS= read -r line; do
    # 500 is UID_MIN value in /etc/login.defs, and it maybe different in various LInux distribution, such as 1000 in Debian
    if test -d "$line"; then
      chmod 400 "$line/.ssh/authorized_keys"
      chmod 500 "$line/.ssh"
    fi
  done

}

function check_and_set_for_root() {
  chmod 400 /root/.ssh/authorized_keys
}

# Check that we are root ... so non-root users stop here
[[ $(id -u) -eq "0" ]] || exit 1

check_and_set_for_common_users
check_and_set_for_root
