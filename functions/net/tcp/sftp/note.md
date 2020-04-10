## FTPS default port
```shell script
# /etc/services 
ftps            990/tcp                 # ftp protocol, control, over TLS/SSL
```
## shell script for FTP/FTPS
```shell script
telnet <server> 990

yum update -y yum ca-certificates openssl openssl-devel curl rpm gnupg2 nss

curl ftp://<server> -u "<user>:<passwd>"

curl --insecure ftps://<server>:<port> -u "<user>:<passwd>"

curl -v --insecure ftps://<server>:<port> -u "<user>:<passwd>"

# ssh port forwarding
ssh -N -f -L <local>:<local port>:<remote>:<remote port> localhost
```
