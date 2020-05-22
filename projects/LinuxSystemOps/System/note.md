## 关于系统资源limits的一些问题

### 关于soft和hard

soft是默认情况（进程不修改soft数值）下，系统允许进程访问的最大资源数。

允许进程在运行时动态修改soft，但不能超过hard，如果超过hard则会报错。

允许用户在程序运行时动态修改进程的soft和hard限制，如：动态调整已经运行中的MySQL的nproc限制
```shell script
echo -n 'Max processes=SOFT_LIMITS:HARD_LIMITS' > /proc/`pidof mysqld`/limits
```

### 关于nproc
在Linux系统中，所有的线程（thread）实则为某种意义上的进程（process），他们的数量都受限于nproc的限制

centos 6.*和centos7可以修改/etc/security/limits.d/90-nproc.conf
>centos 5.*并没有90-nproc.conf这个文件，可直接修改/etc/security/limits.conf，在最后添加
```text
* soft nproc 65535
* hard nproc 65535
```
部分发行版本，如Debian系，可能对root用户有单独的设置，root用户不能使用*代替，如/etc/security/limits.conf中明确说明：
```text
#<domain> can be:
#        - a user name
#        - a group name, with @group syntax
#        - the wildcard *, for default entry
#        - the wildcard %, can be also used with %group syntax,
#                 for maxlogin limit
#        - NOTE: group and wildcard limits are not applied to root.
#          To apply a limit to the root user, <domain> must be
#          the literal username root.
```
