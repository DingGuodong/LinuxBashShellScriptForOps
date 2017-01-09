#!/usr/bin/env bash
# https://www.gnu.org/software/bash/manual/bashref.html#Bash-Variables
# PROMPT_COMMAND
# If set, the value is interpreted as a command to execute before the printing of each primary prompt ($PS1).
# refer 1
echo 'export HISTTIMEFORMAT="%Y-%m-%d %H:%M:%S "' >> /etc/bashrc
echo export PROMPT_COMMAND="'"'{ msg=$(history 1 | { read x y; echo $y; }); user=$(whoami); logger -p local4.info $(date "+%Y-%m-%d %H:%M:%S") "$user" "$msg"; }'"'">> /etc/bashrc
# refer 1 will send message to syslog, depends logger

# refer 2
# Refer: http://dl528888.blog.51cto.com/2382721/1703059
cat >refer2<<'eof'
HISTDIR='/var/log/command.log'
if [ ! -f ${HISTDIR} ];then
touch ${HISTDIR}
chmod 666 ${HISTDIR}
fi
export HISTTIMEFORMAT="{\"TIME\":\"%F %T\",\"HOSTNAME\":\"$HOSTNAME\",\"LI\":\"$(who -u am i 2>/dev/null| awk '{print $NF}'|sed -e 's/[()]//g')\",\"LU\":\"$(who am i|awk '{print $1}')\",\"NU\":\"${USER}\",\"CMD\":\""
export PROMPT_COMMAND="history 1|sed 's/^[ ]\+[0-9]\+  //' | sed 's/$/\"}/'>> /var/log/command.log"
eof
source refer2

# TODO(Guodong Ding) a known bug, using 'refer 2' above will make user confused when a command line include a double quotes(")
    #like this "{"TIME":"2016-05-18 15:43:14", "HOSTNAME":"chris.51devops.com", "IP":"10.20.0.1", "LOGIN":"root", "USER":"root", "CMD":"echo "xxx""}"
    #FIXED: use 'base64' to encoding history
# refer 3  ✓✓✓ **production environment ready**
cat >refer3<<'eof'
HISTDIR='/var/spool/insight'
if [ ! -f ${HISTDIR} ];then
    touch ${HISTDIR}
    chmod 666 ${HISTDIR}
fi
export PROMPT_COMMAND='history 1|sed "s/^[\ 0-9]\+//"| sed "s/^/\{\"TIME\":\"$(date +%F\ %T)\",\"USER\"\:\"$USER\",\"SSH_CLIENT\":\"$(echo $SSH_CLIENT | cut -f1,2 -d " ")\",\"CMD\"\:\"/"|sed "s/$/\"\}/">>${HISTDIR}'
eof

source refer3
rm -f refer3

cat >/etc/profile.d/insight.sh<<'eof'
HISTDIR='/var/spool/insight'
if [ ! -f ${HISTDIR} ];then
    touch ${HISTDIR}
    chmod 666 ${HISTDIR}
fi
export PROMPT_COMMAND='history 1|sed "s/^[\ 0-9]\+//"| sed "s/^/\{\"TIME\":\"$(date +%F\ %T)\",\"USER\"\:\"$USER\",\"SSH_CLIENT\":\"$(echo $SSH_CLIENT | cut -f1,2 -d " ")\",\"CMD\"\:\"/"|sed "s/$/\"\}/">>${HISTDIR}'
eof


tail -f -n20 /var/spool/insight

# TODO(Guodong Ding) using 'refer 3' can not ignore enter key when users type nothing but press enter key, there will be many duplicate content.
# TODO(Guodong Ding) previous history record will be recorded into log file when user login to system.

# refer 4
cat >/etc/profile.d/insight.sh<<'eof'
declare -r HISTDIR='/var/spool/insight'
if [ ! -f ${HISTDIR} ];then
    touch ${HISTDIR}
    chmod 666 ${HISTDIR}
fi
export PROMPT_COMMAND='{ time_now=$(date +%F\ %T); last_history=$(history 1|sed "s/^[\ 0-9]\+//"); real_ip=$(who -m 2>/dev/null| awk "{print \$NF}"|sed -e "s/[()]//g"); ssh_client=$(echo $SSH_CLIENT | cut -f1,2 -d " "); echo "{\"TIME\":\"${time_now}\",\"USER\":\"${USER}\",\"REAL_IP\":\"${real_ip}\",\"SSH_CLIENT\":\"${ssh_client}\",\"CMD\":\"${last_history}\"}">>${HISTDIR}; }'
eof
source /etc/profile.d/insight.sh
tail -n20 -f /var/spool/insight

# export $HISTCONTROL=ignoredups:ignorespace
# /root/.bashrc:HISTCONTROL=ignoredups:ignorespace
# /etc/skel/.bashrc:HISTCONTROL=ignoreboth  # /etc/skel creates standard files for new users
# 'bash -c ""' syntax can NOT execute 'history' command
# bash -c "echo 1|sed s/^[\ ]\+[0-9]\+// | sed s/^/$(echo "xxx")/"|sed 's/$/x/'
# bash -c 'echo 1|sed s/^[\ ]\+[0-9]\+// | sed "s/^/$(echo \{\"TIME\":\"$(date +%F\ %T)\")/"|sed "s/$/\"\}/"'
# bash -c 'echo 1|sed s/^[\ ]\+[0-9]\+// | sed "s/^/$(echo \{\"TIME\":\"$(date +%F\ %T)\",\"USER\"\:\"$USER\",\"SSH_CLIENT\":\"$SSH_CLIENT\",\"CMD\"\:\")/"|sed "s/$/\"\}/"'
# bash -c 'echo 1|sed s/^[\ ]\+[0-9]\+// | sed "s/^/\{\"TIME\":\"$(date +%F\ %T)\",\"USER\"\:\"$USER\",\"SSH_CLIENT\":\"$SSH_CLIENT\",\"CMD\"\:\"/"|sed "s/$/\"\}/"'
# bash -c 'echo 1|sed s/^[\ ]\+[0-9]\+// | sed "s/^/\{\"TIME\":\"$(date +%F\ %T)\",\"USER\"\:\"$USER\",\"SSH_CLIENT\":\"$SSH_CLIENT,$(echo $SSH_CLIENT | cut -f1 -d " ")\",\"CMD\"\:\"/"|sed "s/$/\"\}/"'
# { time_now=$(date +%F\ %T); last_history=$(history 1|sed "s/^[\ 0-9]\+//"); real_ip=$(who -m 2>/dev/null| awk "{print \$NF}"|sed -e "s/[()]//g"); ssh_client=$(echo $SSH_CLIENT | cut -f1,2 -d " "); echo "{\"TIME\":\"${time_now}\",\"USER\":\"${USER}\",\"REAL_IP\":\"${real_ip}\",\"SSH_CLIENT\":\"${ssh_client}\",\"CMD\":\"${last_history}\"}"; }
# bash -c '{ time_now=$(date +%F\ %T); last_history=$(history 1|sed "s/^[\ 0-9]\+//"); real_ip=$(who -m 2>/dev/null| awk "{print \$NF}"|sed -e "s/[()]//g"); ssh_client=$(echo $SSH_CLIENT | cut -f1,2 -d " "); echo "{\"TIME\":\"${time_now}\",\"USER\":\"${USER}\",\"REAL_IP\":\"${real_ip}\",\"SSH_CLIENT\":\"${ssh_client}\",\"CMD\":\"${last_history}\"}"; }'


