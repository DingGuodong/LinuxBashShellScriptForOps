###Find duplicate IP
References:

[How to: Detect Duplicate IP Address With arping command under Linux](http://xmodulo.com/how-to-detect-ip-address-conflicts-in.html)

[How to detect IP address conflicts in Linux](https://www.cyberciti.biz/faq/linux-duplicate-address-detection-with-arping/)

General commands

```bash
apt-get install iputils-arping -y
arping -I eth1 -c 3 192.168.1.1
arping -D -I eth1 -c 2 192.168.1.101
arping -I eth0 192.168.1.101

apt-get install arp-scan -y
arp-scan -I eth1 -l
arp-scan -I eth0 192.168.1.0/24
```
