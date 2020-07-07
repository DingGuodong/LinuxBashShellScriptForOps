
## rsync quick CLI references
```shell script
# rsync all files
sudo /usr/bin/rsync -az -e "ssh -p 22 -oStrictHostKeyChecking=no -i /home/guodong/.ssh/id_rsa" --delete --delete-excluded --log-file=/tmp/rsync.log root@192.168.88.17:/opt/atlassian /opt
# exclude 'backups'
sudo /usr/bin/rsync -az -e "ssh -p 22 -oStrictHostKeyChecking=no -i /home/guodong/.ssh/id_rsa" --delete --delete-excluded --exclude=backups --log-file=/tmp/rsync.log root@192.168.88.17:/opt/atlassian /opt
# rsync a backup
sudo /usr/bin/rsync -a -e "ssh -p 22 -oStrictHostKeyChecking=no -i /home/guodong/.ssh/id_rsa" root@192.168.88.17:/backup/atlassian/application-data/confluence/backups/backup-$(date '+%Y_%m_%d').zip /tmp
```
