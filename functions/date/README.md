All timestamps are returned in ISO 8601 format:
`YYYY-MM-DDTHH:MM:SSZ`

## 关于部分Linux发行版本系统时区的设定
1.确保/etc/localtime正确，也可使用软链接
```bash
diff /etc/localtime /usr/share/zoneinfo/Asia/Shanghai
ln -s /usr/share/zoneinfo/Asia/Shanghai /etc/localtime
```
2.确保时区文件/etc/timezone正确（很多java jvm应用会读取此文件作为系统时区配置，比如Atlassian JIRA）
```bash
$ cat /etc/timezone
Asia/Shanghai
$ 
```

CentOS 6.x/7.x 时区配置

> CentOS 6.x和部分7.x 默认没有/etc/timezone文件

```text
# 以下信息来自`tzselect`
You can make this change permanent for yourself by appending the line
	TZ='Asia/Shanghai'; export TZ
to the file '.profile' in your home directory; then log out and log in again.

# 以下信息来自`man date`
ENVIRONMENT
       TZ     Specifies the timezone, unless overridden by command line parameters.  If neither  is  specified,  the  setting  from
              /etc/localtime is used.
```

> JVM参数（JVM Input Arguments）
>
> -Duser.timezone=Asia/Shanghai

3.验证时区和时间
```shell script
ls -al /etc/localtime
date
timedatectl
tzselect
```
