# Install OpenVPN on Ubuntu Linux
- install OpenVPN Client
```bash
$ sudo apt-get install openvpn
```
- cpoy three files ( **ca.crt your_name.crt **and** yourname.key**) to directory "/etc/openvpn"
- copy \*.ovpn to /etc/openvpn/*your_name*.conf
    *for example:*
    `$ sudo vim /etc/openvpn/config.conf`
    content of "/etc/openvpn/config.conf"is:
    ```bash
client
dev tun
proto tcp
remote 123.126.111.149 10102
resolv-retry infinite
nobind
persist-tun
ca ca.crt
cert your_name.crt
key your_name.key
remote-cert-tls server
comp-lzo adaptive
verb 3
mute 20
```
    **Note: Do not forget to replace your_name to your name.**
    save it using Excape key +":wq"or":x"quit vim editor
- start OpenVPN client service
```bash
$ sudo service openvpn start
$ sudo service openvpn status
```
    **Note: if you didn't see "* VPN 'your_name' is running", you can wait some seconds and try again, otherwise you need check system log "/var/log/syslog"**
- check network connectivity
```bash
$ ping 10.6.28.46
$ ssh 10.6.28.46
```