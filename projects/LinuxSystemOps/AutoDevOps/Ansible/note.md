# Ansible Learning Notes and Best Practices

## benefits

Ansible is an agentless automation tool that by default manages machines over the SSH protocol. 
Once installed, Ansible does not add a database, and there will be no daemons to start or keep running. 
When Ansible manages remote machines, it does not leave software installed or running on them, 
so there’s no real question about how to upgrade Ansible when moving to a new version.

## Ansible Control node

Currently Ansible can be run from any machine with Python 2 (version 2.7) or Python 3 (versions 3.5 and higher) installed. 
This includes Red Hat, Debian, CentOS, macOS, any of the BSDs, and so on. 
Windows is not supported for the control node.

## Ansible Managed node

ssh with sftp enabled and python installed.

## Install Ansible

```shell script
sudo yum install ansible || sudo apt install ansible -y || (
    sudo apt update -y
    sudo apt install software-properties-common -y
    sudo apt-add-repository --yes --update ppa:ansible/ansible
    sudo apt install ansible -y
)

```

## Ansible command shell completion

You can install `python-argcomplete` from EPEL on Red Hat Enterprise based distributions, and or from the standard OS repositories for many other distributions.
```shell script
sudo activate-global-python-argcomplete3
```

## Ansible configuration file

Changes can be made and used in a configuration file which will be searched for in the following order:

   - ANSIBLE_CONFIG (environment variable if set)
    
   - ansible.cfg (in the current directory)
    
   - ~/.ansible.cfg (in the home directory)
    
   - /etc/ansible/ansible.cfg

Ansible will process the above list and use the first file found, all others are ignored.


## Ansible User Guide

[Ansible User Guide](https://docs.ansible.com/ansible/latest/user_guide/index.html)

## Ad-hoc command

### pipe('|') support
shell module support pipe('|'), but command module does not.

```shell script
ansible -i hosts prod -m comamnd -a 'pgrep ftp'
ansible -i hosts prod -a 'pgrep ftp'  # default module is command
ansible -i hosts prod -m shell -a 'ps -ef|grep ftp'
ansible -i hosts prod --become -m raw -a "ps -ef|grep ftp"
``` 

