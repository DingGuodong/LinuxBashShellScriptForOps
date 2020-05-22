## 关于系统资源limits的一些问题

### 关于soft和hard

soft是默认情况（进程不修改soft数值）下，系统允许进程访问的最大资源数。

允许进程在运行时动态修改soft，但不能超过hard，如果超过hard则会报错。

允许用户在程序运行时动态修改进程的soft和hard限制，如：动态调整已经运行中的MySQL的nproc限制
```shell script
echo -n 'Max processes=SOFT_LIMITS:HARD_LIMITS' > /proc/`pidof mysqld`/limits
```
或使用prlimit
>The prlimit system call is supported since Linux 2.6.36, older kernels will break this program.
```shell script
# more examples: man prlimit
prlimit --pid 13134 --rss --nofile=1024:4095
```

### 获取进程运行时的limits
可以通过以下命令查看
```shell script
cat /proc/1/limits
```
或使用prlimit
```shell script
sudo prlimit --pid 1
```

### 关于nproc
在Linux系统中，所有的线程（thread）实则为某种意义上的进程（process），他们的数量都受限于nproc的限制

centos 6.*和centos7可以修改/etc/security/limits.d/90-nproc.conf
>centos 5.*并没有90-nproc.conf这个文件，可直接修改/etc/security/limits.conf，在最后添加
```text
* soft nproc 65535
* hard nproc 65535
```

# 关于/etc/security/limits.conf
/etc/security/limits.conf文件来自pam包，使用PAM的应用都受到此文件中约定的限制。
```text
Name        : pam
Summary     : An extensible library which provides authentication for applications
URL         : http://www.linux-pam.org/
License     : BSD and GPLv2+
Description : PAM (Pluggable Authentication Modules) is a system security tool that
            : allows system administrators to set authentication policy without
            : having to recompile programs that handle authentication.
```

使用PAM的系统应用有crond、sudo、su、bash等。

>可通过命令查看与limits相关联的应用
```shell script
grep pam_limits.so -r /etc/pam.d/
```

除非sshd配置了UsePAM，否则ssh登录启动的进程的limits继承自sshd，而ssh继承自init或systemd。


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
