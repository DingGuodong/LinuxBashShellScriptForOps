## backup policy and best practices

备份策略和最佳实践

> 在常规服务器中，将磁盘区分为系统盘、数据盘和备份盘，除特殊情况外服务部署在数据盘，备份盘用于备份数据盘数据。

不好的备份方法：直接将备份数据备份到备份盘根目录。这样会导致备份盘因故障掉盘后，因为备份盘挂载到根分区的原因，会导致根分区数据写满，从而引发服务异常。

好的备份方法：除了可以监测备份盘的健康状态，还可以将数据备份到备份盘的目录之下，而不是直接将备份数据备份到备份盘根目录（备份盘挂载点）。这样当备份盘掉盘后，不会再写入备份，从而保证不会导致根分区数据写满。

目录结构可以参考**文件系统层次结构标准**：[Filesystem Hierarchy Standard, FHS](https://refspecs.linuxfoundation.org/FHS_3.0/fhs/index.html)

```text
/
├── opt               # Add-on application software packages
├── data              # application data dir
│   ├── app
│   ├── log
│   └── ...
├── backup
│   ├── backup_data   # the directory on backup disk
│   |    └── data
│   |        ├── app
│   |        ├── log
│   |        └── ...
│   └── ...
└── ...
```

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