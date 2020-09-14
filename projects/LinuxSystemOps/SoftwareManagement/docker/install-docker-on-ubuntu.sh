#!/usr/bin/env bash
# https://docs.docker.com/engine/install/ubuntu/

# install docker-ce docker engine with overlay2 storage diver support on Ubuntu(16.04 <= VER <=20.04 LTS) using the repository

# must succeed or die
set -e

# The contents of /var/lib/docker/, including images, containers, volumes, and networks, are preserved.
# The Docker Engine package is now called docker-ce.
sudo apt-get remove -y docker docker-engine docker.io containerd runc

sudo apt-get update -y

sudo apt-get install -y \
apt-transport-https \
ca-certificates \
curl \
gnupg-agent \
software-properties-common

curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -

sudo add-apt-repository \
"deb [arch=amd64] https://download.docker.com/linux/ubuntu \
   $(lsb_release -cs) \
   stable"

sudo apt-get update -y
sudo apt-get install -y docker-ce docker-ce-cli containerd.io

sudo docker version

# https://docs.docker.com/engine/install/linux-postinstall/
sudo usermod -aG docker "$USER"

sudo systemctl enable docker

sudo docker pull hello-world

sudo docker run --rm -it alpine ping -c4 google.com

set +e
