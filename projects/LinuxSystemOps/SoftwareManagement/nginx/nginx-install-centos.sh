#!/usr/bin/env bash
set -e
if ! grep 'Web user' /etc/passwd >/dev/null 2>&1; then
    groupadd -r www
    useradd -r -g www www -c "Web user" -d /dev/null -s /sbin/nologin
fi

NGINX_SOURCE_LATEST_VERSION="nginx-1.12.1"
PCRE_SOURCE_LATEST_VERSION="pcre-8.41"
ZLIB_SOURCE_LATEST_VERSION="zlib-1.2.11"
OPENSSL_SOURCE_LATEST_VERSION="openssl-1.1.0f"

WORKDIR="/tmp/.install_nginx_from_source"
[[ ! -d ${WORKDIR} ]] && mkdir ${WORKDIR}
[[ -d ${WORKDIR} ]] && cd ${WORKDIR}

# http://nchc.dl.sourceforge.net/project/pcre/pcre/8.39/pcre-8.39.tar.gz
[[ ! -f ${WORKDIR}/${NGINX_SOURCE_LATEST_VERSION}.tar.gz ]] && wget -c http://nginx.org/download/${NGINX_SOURCE_LATEST_VERSION}.tar.gz  # http://nginx.org/en/download.html
[[ ! -f ${WORKDIR}/${PCRE_SOURCE_LATEST_VERSION}.tar.gz ]] && wget -c https://ftp.pcre.org/pub/pcre/${PCRE_SOURCE_LATEST_VERSION}.tar.gz  # ftp://ftp.csx.cam.ac.uk/pub/software/programming/pcre/
[[ ! -f ${WORKDIR}/${ZLIB_SOURCE_LATEST_VERSION}.tar.gz ]] && wget -c http://zlib.net/${ZLIB_SOURCE_LATEST_VERSION}.tar.gz  # http://zlib.net/
[[ ! -f ${WORKDIR}/${OPENSSL_SOURCE_LATEST_VERSION}.tar.gz ]] && wget -c https://www.openssl.org/source/${OPENSSL_SOURCE_LATEST_VERSION}.tar.gz  # https://www.openssl.org/source/

tar zxf ${NGINX_SOURCE_LATEST_VERSION}.tar.gz
tar zxf ${PCRE_SOURCE_LATEST_VERSION}.tar.gz
tar zxf ${ZLIB_SOURCE_LATEST_VERSION}.tar.gz
tar zxf ${OPENSSL_SOURCE_LATEST_VERSION}.tar.gz

apt-get -y update
apt-get -y install gcc g++ make

cd ${WORKDIR}/${NGINX_SOURCE_LATEST_VERSION}
./configure --prefix=/usr/local/nginx \
    --with-http_ssl_module \
    --with-stream \
    --user=www --group=www \
    --with-pcre-jit \
    --with-pcre=${WORKDIR}/${PCRE_SOURCE_LATEST_VERSION} \
    --with-zlib=${WORKDIR}/${ZLIB_SOURCE_LATEST_VERSION} \
    --with-openssl=${WORKDIR}/${OPENSSL_SOURCE_LATEST_VERSION}
make && make install

[[ -f /usr/sbin/nginx ]] || ln -s /usr/local/nginx/sbin/nginx /usr/sbin/nginx

nginx -V
nginx -t >/dev/null 2>&1

if [[ -f /usr/local/nginx/logs/nginx.pid ]] && kill -0 `cat /usr/local/nginx/logs/nginx.pid` ; then
    nginx -s stop && nginx
else
    nginx
fi

netstat -anop | grep :80

rm -rf ${WORKDIR}

# /var/lib/python/python3.5_installed
if ! -f ${HOME}/.nginx_installed ; then

tee /usr/local/nginx/conf/nginx.conf<<-'eof'
user www;
worker_processes  auto;
worker_rlimit_nofile 200000;
error_log logs/error.log notice;
pid        logs/nginx.pid;
events {
    use epoll;
    worker_connections  51200;
    multi_accept on;
}
http {
    include        mime.types;
    client_body_timeout 10s;
    default_type   application/octet-stream;
    sendfile       on;
    send_timeout   2s;
    tcp_nodelay    on;
    tcp_nopush     on;
    keepalive_timeout  65;
    keepalive_requests 200000;
    reset_timedout_connection on;
    server_tokens off;
    gzip  on;
    gzip_min_length 10240;
    gzip_proxied expired no-cache no-store private auth;
    gzip_types text/plain text/css text/xml text/javascript application/x-javascript application/xml;
    gzip_disable "MSIE [1-6]\.";
    gzip_vary on;
    access_log     off;
    open_file_cache max=200000 inactive=20s;
    open_file_cache_valid    30s;
    open_file_cache_min_uses 2;
    open_file_cache_errors   on;
    log_format  main  '$remote_addr - $remote_user [$time_local] "$request" '
              '$status $body_bytes_sent "$http_referer" '
              '"$http_user_agent" "$http_x_forwarded_for"';
include conf.d/*.conf;
}
eof
test -d /usr/local/nginx/conf/conf.d && test ! -h /usr/local/nginx/conf/conf.d && rm -r /usr/local/nginx/conf/conf.d/
mkdir -p /usr/local/nginx/conf/vhost
ln -s /usr/local/nginx/conf/vhost /usr/local/nginx/conf/conf.d
tee /usr/local/nginx/conf/vhost/default.conf<<-eof
server {
        listen       80;
        server_name  localhost;

        access_log  logs/http_default.access.log  main;

        location / {
            root   html;
            index  index.html index.htm;
        }

        error_page   500 502 503 504  /50x.html;
        location = /50x.html {
            root   html;
        }

    }
eof
wget http://nginx.org/favicon.ico -O /usr/local/nginx/html/favicon.ico
nginx -t && sudo nginx -s reload

touch ${HOME}/.nginx_installed
fi

set +e