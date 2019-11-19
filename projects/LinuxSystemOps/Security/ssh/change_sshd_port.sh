#!/usr/bin/env bash
# change ssh service port and restart it

# change ssh service port to a random and unused port between 1001 and 65534
function change_sshd_port() {
  sshd_port=$RANDOM

  netstat -lt | grep :$sshd_port
  ret_value=$?

  while [[ $sshd_port -lt 1000 && $sshd_port -gt 65535 && $ret_value != 0 ]]; do
    sshd_port=$RANDOM
  done

  intranet_ip=$(ip addr show scope global "$(ip route | awk '/^default/ {print $5}')" | awk -F '[ /]+' '/global/ {print $3}')

  echo -e "\033[01;34mwait for getting ip info from internet...\033[0m"
  echo -e "current internet ip address is: \033[01;32m$(curl -s https://ifconfig.io)\033[0m"
  echo -e "current intranet ip address is: \033[01;32m$intranet_ip\033[0m"

  if test "$(awk '/^Port 22/' /etc/ssh/sshd_config)" == "Port 22"; then
    cp /etc/ssh/sshd_config /etc/ssh/sshd_config"$(date +%Y%m%d%H%M%S)"~
    sed -i "s/^Port 22/Port $sshd_port/g" /etc/ssh/sshd_config
    echo -e "new sshd port is: \033[01;31m$sshd_port\033[0m"
  elif grep ^Port /etc/ssh/sshd_config >&/dev/null; then
    echo -e "skipped, sshd port in not 22, current sshd port is: \033[01;31m$(sed -n '/^Port/p' /etc/ssh/sshd_config | awk '{print $2}')\033[0m"
  else
    cp /etc/ssh/sshd_config /etc/ssh/sshd_config"$(date +%Y%m%d%H%M%S)"~
    sed -i "$ a Port $sshd_port" /etc/ssh/sshd_config
    echo -e "new sshd port is: \033[01;31m$sshd_port\033[0m"
  fi
}

# restart ssh servie with service manager
function restart_ssh_service() {
  echo -e "\033[01;34mwait for ssh service restart...\033[0m"

  if [[ -f /etc/init.d/ssh ]]; then
    /etc/init.d/ssh restart || systemctl restart ssh.service
  elif [[ -f /etc/init.d/sshd ]]; then
    /etc/init.d/sshd restart || systemctl restart sshd.service
  fi

  if netstat -lnt | grep :$sshd_port >&/dev/null; then
    echo -e "\033[01;32mssh service restarted successfully.\033[0m"
    echo -e "\033[01;33mit will take effect after you next login.\033[0m"
  else
    echo -e "\033[01;31mError: ssh service restarted failed.\033[0m"
    pgrep sshd
    /etc/init.d/sshd status || systemctl status sshd.service
  fi

}

# Check that we are root ... so non-root users stop here
[[ $(id -u) -eq "0" ]] || echo -e "\033[01;31myou would have to be root to run it.\033[0m" && exit 1

change_sshd_port
restart_ssh_service
