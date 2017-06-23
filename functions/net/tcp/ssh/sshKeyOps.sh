#!/usr/bin/env bash
exit 0

cd
ssh-keygen -N "" -f /root/.ssh/id_rsa
cd /root/.ssh/
[[ ! -e /root/.ssh/authorized_keys ]] && cp id_rsa.pub authorized_keys
cat >>authorized_keys<<eof
ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQCawuOgQup3Qc1OILytyH+u3S9te85ctEKTvzPtRjHfnEEOjpRS6v6/PsuDHplHO1PAm8cKbEZmqR9tg4mWSweosBYW7blUUB4yWfBu6cHAnJOZ7ADNWHHJHAYi8QFZd4SLAAKbf9J12Xrkw2qZkdUyTBVbm+Y8Ay9bHqGX7KKLhjt0FIqQHRizcvncBFHXbCTJWsAduj2i7GQ5vJ507+MgFl2ZTKD2BGX5m0Jq9z3NTJD7fEb2J6RxC9PypYjayXyQBhgACxaBrPXRdYVXmy3f3zRQ4/OmJvkgoSodB7fYL8tcUZWSoXFa33vdPlVlBYx91uuA6onvOXDnryo3frN1
ssh-rsa AAAAB3NzaC1yc2EAAAABJQAAAIEAumQ2srRwd9slaeYTdr/dGd0H4NzJ3uQdBQABTe/nhJsUFWVG3titj7JiOYjCb54dmpHoi4rAYIElwrolQttZSCDKTVjamnzXfbV8HvJapLLLJTdKraSXhiUkdS4D004uleMpaqhmgNxCLu7onesCCWQzsNw9Hgpx5Hicpko6Xh0=
eof
cd

cd
[ ! -d /root/.ssh ] && mkdir /root/.ssh
[ ! -e /root/.ssh/authorized_keys ] && touch /root/.ssh/authorized_keys
cat >>/root/.ssh/authorized_keys<<eof
ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQCawuOgQup3Qc1OILytyH+u3S9te85ctEKTvzPtRjHfnEEOjpRS6v6/PsuDHplHO1PAm8cKbEZmqR9tg4mWSweosBYW7blUUB4yWfBu6cHAnJOZ7ADNWHHJHAYi8QFZd4SLAAKbf9J12Xrkw2qZkdUyTBVbm+Y8Ay9bHqGX7KKLhjt0FIqQHRizcvncBFHXbCTJWsAduj2i7GQ5vJ507+MgFl2ZTKD2BGX5m0Jq9z3NTJD7fEb2J6RxC9PypYjayXyQBhgACxaBrPXRdYVXmy3f3zRQ4/OmJvkgoSodB7fYL8tcUZWSoXFa33vdPlVlBYx91uuA6onvOXDnryo3frN1
ssh-rsa AAAAB3NzaC1yc2EAAAABJQAAAIEAumQ2srRwd9slaeYTdr/dGd0H4NzJ3uQdBQABTe/nhJsUFWVG3titj7JiOYjCb54dmpHoi4rAYIElwrolQttZSCDKTVjamnzXfbV8HvJapLLLJTdKraSXhiUkdS4D004uleMpaqhmgNxCLu7onesCCWQzsNw9Hgpx5Hicpko6Xh0=
eof
cat /root/.ssh/authorized_keys
cd

cat >/root/.ssh/authorized_keys<<eof
ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQCawuOgQup3Qc1OILytyH+u3S9te85ctEKTvzPtRjHfnEEOjpRS6v6/PsuDHplHO1PAm8cKbEZmqR9tg4mWSweosBYW7blUUB4yWfBu6cHAnJOZ7ADNWHHJHAYi8QFZd4SLAAKbf9J12Xrkw2qZkdUyTBVbm+Y8Ay9bHqGX7KKLhjt0FIqQHRizcvncBFHXbCTJWsAduj2i7GQ5vJ507+MgFl2ZTKD2BGX5m0Jq9z3NTJD7fEb2J6RxC9PypYjayXyQBhgACxaBrPXRdYVXmy3f3zRQ4/OmJvkgoSodB7fYL8tcUZWSoXFa33vdPlVlBYx91uuA6onvOXDnryo3frN1
ssh-rsa AAAAB3NzaC1yc2EAAAABJQAAAIEAumQ2srRwd9slaeYTdr/dGd0H4NzJ3uQdBQABTe/nhJsUFWVG3titj7JiOYjCb54dmpHoi4rAYIElwrolQttZSCDKTVjamnzXfbV8HvJapLLLJTdKraSXhiUkdS4D004uleMpaqhmgNxCLu7onesCCWQzsNw9Hgpx5Hicpko6Xh0=
eof

 history -c && exit

# Multi host register SSH key 1
# ssh-keygen -N "" -f /root/.ssh/id_rsa
[ ! -e /root/.ssh/authorized_keys ] && mkdir /root/.ssh
# ssh-keyscan 192.168.1.241 192.168.1.242 192.168.1.243 |& awk -F '[ ]+' '!/^#/ {print $2" "$3}' >> /root/.ssh/authorized_keys
ssh-keyscan -t rsa 192.168.1.241 192.168.1.242 192.168.1.243 |& awk -F '[ ]+' '!/^#/ {print $2" "$3}' >> /root/.ssh/authorized_keys
ssh -i /etc/ssh/ssh_host_rsa_key -p 22 -oStrictHostKeyChecking=no root@192.168.1.242 "uname -a"

# Multi host register SSH key 2
# ssh-keygen -N "" -f /root/.ssh/id_rsa
[ ! -e /root/.ssh/authorized_keys ] && mkdir /root/.ssh
# ssh-keyscan 192.168.1.241 192.168.1.242 192.168.1.243 |& awk -F '[ ]+' '!/^#/ {print $2" "$3}' >> /root/.ssh/authorized_keys
if grep -v "trust host ssh key" /root/.ssh/authorized_keys >/dev/null ; then
  echo "trust host ssh key lists, begin" >> /root/.ssh/authorized_keys
  ssh-keyscan -t rsa 10.6.28.46 10.6.28.135 10.6.28.27 10.6.28.125 10.6.28.28 10.6.28.35 10.6.28.93 |& awk -F '[ ]+' '!/^#/ {print $2" "$3}' >> /root/.ssh/authorized_keys
  echo "trust host ssh key lists, end" >> /root/.ssh/authorized_keys
fi
ssh -i /etc/ssh/ssh_host_rsa_key -p 22 -oStrictHostKeyChecking=no root@10.6.28.46 "uname -a"

# scp
nohup scp -i /etc/ssh/ssh_host_rsa_key -oStrictHostKeyChecking=no -rp /data root@10.144.138.248:/data/backup/data_directory_from_42.96.187.191 >/tmp/.log_backup_$$_$RANDOM 2>&1 &
