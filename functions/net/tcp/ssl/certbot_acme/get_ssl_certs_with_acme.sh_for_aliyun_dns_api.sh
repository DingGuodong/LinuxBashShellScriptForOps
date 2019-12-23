#!/usr/bin/env bash
# use acme.sh to get Let's Encrypt HTTPS certificates

# A pure Unix shell script implementing ACME client protocol
# https://github.com/Neilpang/acme.sh
# https://github.com/Neilpang/acme.sh/wiki/dnsapi

aliyun_dns_access_key="your access key"
aliyun_dns_secret="your secret"
domain_name="example.com"

if [ "$(id -u)" != "0" ]; then
    echo "Error: You must be root to run this script."
    exit 1
fi

export Ali_Key="$aliyun_dns_access_key"
export Ali_Secret="$aliyun_dns_secret"

git clone https://github.com/Neilpang/acme.sh.git
cd ./acme.sh || exit
./acme.sh --install
crontab -l
. /root/.bashrc || . "/root/.acme.sh/acme.sh.env"

acme.sh --issue -d "$domain_name"  -d "*.$domain_name" --dns dns_ali
ls /root/.acme.sh/"$domain_name"/"$domain_name".cer
ls /root/.acme.sh/"$domain_name"/"$domain_name".key
cat /root/.acme.sh/account.conf

