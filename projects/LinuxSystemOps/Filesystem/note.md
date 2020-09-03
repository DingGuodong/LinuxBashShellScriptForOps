
## rsync
Rsync is widely used for backups and mirroring and as an improved copy command for everyday use.

## rsync quick CLI references
```shell script
# rsync all files
sudo /usr/bin/rsync -az -e "ssh -p 22 -oStrictHostKeyChecking=no -i /home/guodong/.ssh/id_rsa" --delete --delete-excluded --log-file=/tmp/rsync.log root@192.168.88.17:/opt/atlassian /opt
# exclude 'backups'
sudo /usr/bin/rsync -az -e "ssh -p 22 -oStrictHostKeyChecking=no -i /home/guodong/.ssh/id_rsa" --delete --delete-excluded --exclude=backups --log-file=/tmp/rsync.log root@192.168.88.17:/opt/atlassian /opt
# rsync a backup
sudo /usr/bin/rsync -a -e "ssh -p 22 -oStrictHostKeyChecking=no -i /home/guodong/.ssh/id_rsa" root@192.168.88.17:/backup/atlassian/application-data/confluence/backups/backup-$(date '+%Y_%m_%d').zip /tmp
```

## How does rsync find files that need to be transferred? -- "quick check" algorithm 
Rsync finds files that need to be transferred using a "quick check" algorithm (by default) that looks for files that have changed in size or in last-modified time.
Any changes in the other preserved attributes (as requested by options) are made on the destination file directly when the quick check indicates that the file's data does not need to be updated.

The option turns off rsync's "quick check" algorithm 
```
--ignore-times, -I
--size-only
--checksum, -c  # this option can be used in some more severe scenario but it will slow performance if there are many files to handle
```

notes: Generating the checksums means that both sides will expend a lot of disk I/O reading all the data 
in the files in the transfer, so this can slow things down significantly.