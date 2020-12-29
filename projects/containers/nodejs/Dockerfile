# [Official Node.js Docker Image](https://hub.docker.com/_/node/)
# [Official Debian Docker Image](https://hub.docker.com/_/debian/)
# [Dockerfile reference](https://docs.docker.com/engine/reference/builder/)

# docker rum --rm -it debian:buster /bin/bash

FROM debian:buster

ENV NODE_VERSION=12.16.3

ENV YARN_VERSION=1.22.10

# modify apt sources, note: use HTTP protocol as possible, 'Certificate verification failed:The certificate is NOT trusted.'
RUN /bin/sed -i 's@http://deb.debian.org/debian@[trusted=yes] http://mirrors.aliyun.com/debian@g' /etc/apt/sources.list && /bin/sed -i 's@http://security.debian.org/debian-security@[trusted=yes] http://mirrors.aliyun.com/debian-security@g' /etc/apt/sources.list

RUN /bin/sh -c set -eux; apt-get update; apt-get install -y --no-install-recommends ca-certificates curl netbase wget xz-utils unzip apt-utils; rm -rf /var/lib/apt/lists/*

RUN  /bin/sh -c set -ex; if ! command -v gpg > /dev/null; then apt-get update; apt-get install -y --no-install-recommends gnupg dirmngr;rm -rf /var/lib/apt/lists/*; fi

RUN  /bin/sh -c set -ex; apt-get update && apt-get install -y --no-install-recommends bzr git mercurial openssh-client subversion procps && rm -rf /var/lib/apt/lists/*

RUN  /bin/sh -c set -ex; apt-get update; apt-get install -y --no-install-recommends autoconf automake bzip2 dpkg-dev file g++ gcc imagemagick libbz2-dev libc6-dev libcurl4-openssl-dev libdb-dev libevent-dev libffi-dev libgdbm-dev libglib2.0-dev libgmp-dev libjpeg-dev libkrb5-dev liblzma-dev libmagickcore-dev libmagickwand-dev libmaxminddb-dev libncurses5-dev libncursesw5-dev libpng-dev libpq-dev libreadline-dev libsqlite3-dev libssl-dev libtool libwebp-dev libxml2-dev libxslt-dev libyaml-dev make patch unzip xz-utils zlib1g-dev $(if apt-cache show 'default-libmysqlclient-dev' 2>/dev/null | grep -q '^Version:'; then echo 'default-libmysqlclient-dev'; 	else echo 'libmysqlclient-dev'; fi ); rm -rf /var/lib/apt/lists/*

RUN  /bin/sh -c "groupadd --gid 1000 node && useradd --uid 1000 --gid node --shell /bin/bash --create-home node"

RUN  /bin/sh -c ARCH= && dpkgArch="$(dpkg --print-architecture)" && case "${dpkgArch##*-}" in amd64) ARCH='x64';; ppc64el) ARCH='ppc64le';; s390x) ARCH='s390x';; arm64) ARCH='arm64';; armhf) ARCH='armv7l';; i386) ARCH='x86';; *) echo "unsupported architecture"; exit 1 ;; esac && set -ex && for key in 4ED778F539E3634C779C87C6D7062848A1AB005C 94AE36675C464D64BAFA68DD7434390BDBE9B9C5 1C050899334244A8AF75E53792EF661D867B9DFA 71DCFD284A79C3B38668286BC97EC7A07EDE3FC1 8FCCA13FEF1D0C2E91008E09770F7A9A5AE15600 C4F0DFFF4E8C1A8236409D08E73BC641CC11F4C8 C82FA3AE1CBEDC6BE46B9360C43CEC45C17AB93C DD8F2338BAE7501E3DD5AC78C273792F7D83545D A48C2BEE680E841632CD4E44F07496B3EB3C1762 108F52B48DB57BB0CC439B2997B01419BD92F80A B9E2F5981AA6E0CD28160D9FF13993A75599653C ; do gpg --batch --keyserver hkp://p80.pool.sks-keyservers.net:80 --recv-keys "$key" || gpg --batch --keyserver hkp://ipv4.pool.sks-keyservers.net --recv-keys "$key" || gpg --batch --keyserver hkp://pgp.mit.edu:80 --recv-keys "$key" ; done && curl -fsSLO --compressed "https://nodejs.org/dist/v$NODE_VERSION/node-v$NODE_VERSION-linux-$ARCH.tar.xz" && curl -fsSLO --compressed "https://nodejs.org/dist/v$NODE_VERSION/SHASUMS256.txt.asc" && gpg --batch --decrypt --output SHASUMS256.txt SHASUMS256.txt.asc && grep " node-v$NODE_VERSION-linux-$ARCH.tar.xz\$" SHASUMS256.txt | sha256sum -c - && tar -xJf "node-v$NODE_VERSION-linux-$ARCH.tar.xz" -C /usr/local --strip-components=1 --no-same-owner && rm "node-v$NODE_VERSION-linux-$ARCH.tar.xz" SHASUMS256.txt.asc SHASUMS256.txt && ln -s /usr/local/bin/node /usr/local/bin/nodejs && node --version && npm --version

RUN  /bin/sh -c set -ex && for key in 6A010C5166006599AA17F08146C2130DFD2497F5 ; do gpg --batch --keyserver hkp://p80.pool.sks-keyservers.net:80 --recv-keys "$key" || gpg --batch --keyserver hkp://ipv4.pool.sks-keyservers.net --recv-keys "$key" || gpg --batch --keyserver hkp://pgp.mit.edu:80 --recv-keys "$key" ; done && curl -fsSLO --compressed "https://yarnpkg.com/downloads/$YARN_VERSION/yarn-v$YARN_VERSION.tar.gz" && curl -fsSLO --compressed "https://yarnpkg.com/downloads/$YARN_VERSION/yarn-v$YARN_VERSION.tar.gz.asc" && gpg --batch --verify yarn-v$YARN_VERSION.tar.gz.asc yarn-v$YARN_VERSION.tar.gz && mkdir -p /opt && tar -xzf yarn-v$YARN_VERSION.tar.gz -C /opt/ && ln -s /opt/yarn-v$YARN_VERSION/bin/yarn /usr/local/bin/yarn && ln -s /opt/yarn-v$YARN_VERSION/bin/yarnpkg /usr/local/bin/yarnpkg && rm yarn-v$YARN_VERSION.tar.gz.asc yarn-v$YARN_VERSION.tar.gz && yarn --version

COPY docker-entrypoint.sh /usr/local/bin

ENTRYPOINT ["docker-entrypoint.sh"]

CMD ["node"]
