## create a container from ubuntu with ssh support
create a Dockerfile
```shell script
mkdir dockerfile && cd dockerfile && vim Dockerfile
```

Dockerfile content
```dockerfile
FROM ubuntu:latest
RUN apt-get update -y \
    && apt-get install openssh-server -y \
    && mkdir -p ~/.ssh /run/sshd \
    && ssh-keygen -N "" -f ~/.ssh/id_rsa \
    && cp ~/.ssh/id_rsa.pub ~/.ssh/authorized_keys
EXPOSE 22 80 443
CMD ["/usr/sbin/sshd", "-D"]
```

build image, run and try ssh it
> Attention: In production environment, do NOT use 'latest' tag for image unless you know what does it mean.
> You should use a specific version number, such as '20.9.1'.
```shell script
docker build -t ubuntu_sshd:latest .
cd
docker run -dit \
  --name 'ubuntu20' --hostname 'ubuntu20' \
  -v /etc/localtime:/etc/localtime:ro \
  -p 2022:22 \
  -p 2080:80 \
  -p 20443:443 \
  ubuntu_sshd:latest
docker cp ubuntu20:/root/.ssh/id_rsa ubuntu20_ssh_id_rsa
# ssh-keygen -f "/home/guodong/.ssh/known_hosts" -R "$(docker inspect --format='{{.NetworkSettings.IPAddress}}' ubuntu20)"
ssh -i ubuntu20_ssh_id_rsa -oStrictHostKeyChecking=no root@$(docker inspect --format='{{.NetworkSettings.IPAddress}}' ubuntu20) uname -a
```

## create a container from centos with ssh support
create a Dockerfile
```shell script
mkdir -p dockerfile && cd dockerfile && vim Dockerfile
```

Dockerfile content
```dockerfile
FROM centos:latest
RUN yum update -y \
    && yum install openssh-server -y \
    && mkdir -p ~/.ssh /run/sshd \
    && ssh-keygen -A \
    && ssh-keygen -N "" -f ~/.ssh/id_rsa \
    && cp ~/.ssh/id_rsa.pub ~/.ssh/authorized_keys
EXPOSE 22 80 443
CMD ["/usr/sbin/sshd", "-D"]
```

build image, run and try ssh it
> Attention: In production environment, do NOT use 'latest' tag for image unless you know what does it mean.
> You should use a specific version number, such as '20.9.1'.
```shell script
docker build -t centos_sshd:latest .
cd
docker run -dit \
  --name 'centos' --hostname 'centos' \
  -v /etc/localtime:/etc/localtime:ro \
  -p 2122:22 \
  -p 2180:80 \
  -p 21443:443 \
  centos_sshd:latest
docker cp centos:/root/.ssh/id_rsa centos_ssh_id_rsa
# ssh-keygen -f "/home/guodong/.ssh/known_hosts" -R "$(docker inspect --format='{{.NetworkSettings.IPAddress}}' centos)"
ssh -i centos_ssh_id_rsa -oStrictHostKeyChecking=no root@$(docker inspect --format='{{.NetworkSettings.IPAddress}}' centos) uname -a
```
