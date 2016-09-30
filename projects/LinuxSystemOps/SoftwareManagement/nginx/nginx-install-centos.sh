#!/usr/bin/env bash
set -e
if ! grep 'Web user' /etc/passwd >/dev/null 2>&1; then
    groupadd -r www
    useradd -r -g www www -c "Web user" -d /dev/null -s /sbin/nologin
fi


NGINX_SOURCE_LATEST_VERSION="nginx-1.10.1"
PCRE_SOURCE_LATEST_VERSION="pcre-8.39"
ZLIB_SOURCE_LATEST_VERSION="zlib-1.2.8"
OPENSSL_SOURCE_LATEST_VERSION="openssl-1.1.0b"


WORKDIR="/tmp/.install_nginx_from_source"
[ ! -d ${WORKDIR} ] && mkdir ${WORKDIR}
[ -d ${WORKDIR} ] && cd ${WORKDIR}


# http://nchc.dl.sourceforge.net/project/pcre/pcre/8.39/pcre-8.39.tar.gz
[ ! -f ${WORKDIR}/${NGINX_SOURCE_LATEST_VERSION}.tar.gz ] && wget -c http://nginx.org/download/${NGINX_SOURCE_LATEST_VERSION}.tar.gz  # http://nginx.org/en/download.html
[ ! -f ${WORKDIR}/${PCRE_SOURCE_LATEST_VERSION}.tar.gz ] && wget -c ftp://ftp.csx.cam.ac.uk/pub/software/programming/pcre/${PCRE_SOURCE_LATEST_VERSION}.tar.gz  # ftp://ftp.csx.cam.ac.uk/pub/software/programming/pcre/
[ ! -f ${WORKDIR}/${ZLIB_SOURCE_LATEST_VERSION}.tar.gz ] && wget -c http://zlib.net/${ZLIB_SOURCE_LATEST_VERSION}.tar.gz  # http://zlib.net/
[ ! -f ${WORKDIR}/${OPENSSL_SOURCE_LATEST_VERSION}.tar.gz ] && wget -c https://www.openssl.org/source/${OPENSSL_SOURCE_LATEST_VERSION}.tar.gz  # https://www.openssl.org/source/


tar zxf ${NGINX_SOURCE_LATEST_VERSION}.tar.gz
tar zxf ${PCRE_SOURCE_LATEST_VERSION}.tar.gz
tar zxf ${ZLIB_SOURCE_LATEST_VERSION}.tar.gz
tar zxf ${OPENSSL_SOURCE_LATEST_VERSION}.tar.gz

apt-get -y update
apt-get -y install gcc g++ make


cd nginx-1.10.1
./configure --prefix=/usr/local/nginx \
    --with-http_ssl_module \
    --with-stream \
    --user=www --group=www \
    --with-pcre-jit \
    --with-pcre=${WORKDIR}/${PCRE_SOURCE_LATEST_VERSION} \
    --with-zlib=${WORKDIR}/${ZLIB_SOURCE_LATEST_VERSION} \
    --with-openssl=${WORKDIR}/${OPENSSL_SOURCE_LATEST_VERSION}
make && make install
ln -s /usr/local/nginx/sbin/nginx /usr/sbin/nginx


nginx -V
nginx -t >/dev/null 2>&1 && nginx && netstat -anop | grep :80


set +e