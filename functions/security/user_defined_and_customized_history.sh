#!/usr/bin/env bash

# refer 1
echo 'export HISTTIMEFORMAT="%Y-%m-%d %H:%M:%S "' >> /etc/bashrc
echo export PROMPT_COMMAND="'"'{ msg=$(history 1 | { read x y; echo $y; }); user=$(whoami); logger -p local4.info $(date "+%Y-%m-%d %H:%M:%S") "$user" "$msg"; }'"'">> /etc/bashrc

# refer 2
# Refer: http://dl528888.blog.51cto.com/2382721/1703059
cat >testfile_1<<EOF
HISTDIR='/var/log/command.log'
if [ ! -f \$HISTDIR ];then
touch \$HISTDIR
chmod 666 \$HISTDIR
fi
export HISTTIMEFORMAT="{\"TIME\":\"%F %T\",\"HOSTNAME\":\"\$HOSTNAME\",\"LI\":\"\$(who -u am i 2>/dev/null| awk '{print \$NF}'|sed -e 's/[()]//g')\",\"LU\":\"\$(who am i|awk '{print \$1}')\",\"NU\":\"\${USER}\",\"CMD\":\""
export PROMPT_COMMAND='history 1|tail -1|sed "s/^[ ]\+[0-9]\+  //"|sed "s/$/\"}/">> /var/log/command.log'
EOF

true > testfile_2 && vim testfile_2
HISTDIR='/var/log/command.log'
if [ ! -f $HISTDIR ];then
touch $HISTDIR
chmod 666 $HISTDIR
fi
export HISTTIMEFORMAT="{\"TIME\":\"%F %T\",\"HOSTNAME\":\"$HOSTNAME\",\"LI\":\"$(who -u am i 2>/dev/null| awk '{print $NF}'|sed -e 's/[()]//g')\",\"LU\":\"$(who am i|awk '{print $1}')\",\"NU\":\"${USER}\",\"CMD\":\""
export PROMPT_COMMAND='history 1|tail -1|sed "s/^[ ]\+[0-9]\+  //"|sed "s/$/\"}/">> /var/log/command.log'

diff testfile_1 testfile_2

# TODO(Guodong Ding) a known bug, using 'refer 2' above will make user confused when a command line include a double quotes(")
    #   like this "{"TIME":"2016-05-18 15:43:14", "HOSTNAME":"chris.51devops.com", "IP":"10.20.0.1", "LOGIN":"root", "USER":"root", "CMD":"export PROMPT_COMMAND='history 1|tail -1|sed "s/^[ ]\+[0-9]\+  //"|sed "s/^/{/"|sed "s/$/\"}/">> /var/log/command.log'"}"
