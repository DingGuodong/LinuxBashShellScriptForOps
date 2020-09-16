# Inventory
Ansible works against multiple systems in your infrastructure at the same time. 
It does this by selecting portions of systems listed in Ansible’s inventory file, 
which defaults to being saved in the location /etc/ansible/hosts. 
You can specify a different inventory file using the -i <path> option on the command line.

## Hosts and Groups
[Hosts and Groups](http://docs.ansible.com/ansible/intro_inventory.html#hosts-and-groups)

Create Ansible’s inventory file
```bash
ansible_default_location="/etc/ansible"
ansible_default_inventory_file="$ansible_default_location/hosts"
test ! -d ${ansible_default_location} && mkdir ${ansible_default_location}
test ! -f ${ansible_default_inventory_file} && cat>${ansible_default_inventory_file}<<'eof'
192.168.100.101 ansible_connection=ssh ansible_host=192.168.100.101 ansible_port=22 ansible_user=root ansible_ssh_private_key_file=/etc/ssh/ssh_host_rsa_key ansible_ssh_common_args="-oStrictHostKeyChecking=no"
192.168.100.122 ansible_user=root ansible_ssh_private_key_file=/etc/ssh/ssh_host_rsa_key ansible_ssh_common_args="-oStrictHostKeyChecking=no"
192.168.100.123 ansible_user=root ansible_ssh_private_key_file=/etc/ssh/ssh_host_rsa_key ansible_ssh_common_args="-oStrictHostKeyChecking=no"
192.168.100.124 ansible_user=root ansible_ssh_private_key_file=/etc/ssh/ssh_host_rsa_key ansible_ssh_common_args="-oStrictHostKeyChecking=no"
192.168.100.125 ansible_user=root ansible_ssh_private_key_file=/etc/ssh/ssh_host_rsa_key ansible_ssh_common_args="-oStrictHostKeyChecking=no"
192.168.100.126 ansible_user=root ansible_ssh_private_key_file=/etc/ssh/ssh_host_rsa_key ansible_ssh_common_args="-oStrictHostKeyChecking=no"
192.168.100.127 ansible_user=root ansible_ssh_private_key_file=/etc/ssh/ssh_host_rsa_key ansible_ssh_common_args="-oStrictHostKeyChecking=no"
192.168.100.128 ansible_user=root ansible_ssh_private_key_file=/etc/ssh/ssh_host_rsa_key ansible_ssh_common_args="-oStrictHostKeyChecking=no"
192.168.100.129 ansible_user=root ansible_ssh_private_key_file=/etc/ssh/ssh_host_rsa_key ansible_ssh_common_args="-oStrictHostKeyChecking=no"
192.168.100.130 ansible_user=root ansible_ssh_private_key_file=/etc/ssh/ssh_host_rsa_key ansible_ssh_common_args="-oStrictHostKeyChecking=no"
eof
```

```text
mail.example.com

[webservers]
foo.example.com
bar.example.com ansible_connection=ssh ansible_host=192.168.1.200 ansible_port=22 ansible_user=root ansible_ssh_private_key_file=/etc/ssh/ssh_host_rsa_key
www[01:50].example.com

[dbservers]
one.example.com
two.example.com
three.example.com
db-[a:f].example.com
```
[List of Behavioral Inventory Parameters](http://docs.ansible.com/ansible/intro_inventory.html#list-of-behavioral-inventory-parameters)

## Test commands 
```bash
ansible all -a 'w'
```

Or you can execute some Ad-Hoc Commands
[Ad-Hoc Commands](http://docs.ansible.com/ansible/intro_adhoc.html#introduction-to-ad-hoc-commands)

Test commands examples:
```bash
# Using the shell - Execute commands in nodes. module looks like this:
# [shell - Execute commands in nodes](http://docs.ansible.com/ansible/shell_module.html#shell-execute-commands-in-nodes)
# [About Modules](http://docs.ansible.com/ansible/modules.html#about-modules)
ansible raleigh -m shell -a 'echo $TERM'
ansible -i hosts prod -a "uname -a"
ansible -i hosts test -m command -a "uname -a"
ansible -i hosts nginx -m shell -a "uname -a"

# To transfer a file directly to many servers:
ansible atlanta -m copy -a "src=/etc/hosts dest=/tmp/hosts"
ansible webservers -m file -a "dest=/srv/foo/a.txt mode=600"
ansible webservers -m file -a "dest=/srv/foo/b.txt mode=600 owner=mdehaan group=mdehaan"
# The file module can also create directories, similar to mkdir -p:
ansible webservers -m file -a "dest=/path/to/c mode=755 owner=mdehaan group=mdehaan state=directory"
# As well as delete directories (recursively) and delete files:
ansible webservers -m file -a "dest=/path/to/c state=absent"
# Managing Packages
ansible webservers -m yum -a "name=acme state=present"
ansible webservers -m yum -a "name=acme-1.5 state=present"
ansible webservers -m yum -a "name=acme state=latest"
ansible webservers -m yum -a "name=acme state=absent"
# Users and Groups
ansible all -m user -a "name=foo password=<crypted password here>"
ansible all -m user -a "name=foo state=absent"
# Deploying From Source Control
ansible webservers -m git -a "repo=git://foo.example.org/repo.git dest=/srv/myapp version=HEAD"
# Managing Services
ansible webservers -m service -a "name=httpd state=started"
ansible webservers -m service -a "name=httpd state=restarted"
ansible webservers -m service -a "name=httpd state=stopped"
# [Time Limited Background Operations](http://docs.ansible.com/ansible/intro_adhoc.html#time-limited-background-operations)
ansible all -B 3600 -P 0 -a "/usr/bin/long_running_operation --do-stuff"
ansible web1.example.com -m async_status -a "jid=488359678239.2844"
ansible all -B 1800 -P 60 -a "/usr/bin/long_running_operation --do-stuff"
# Gathering Facts
# [Variables](http://docs.ansible.com/ansible/playbooks_variables.html)
ansible all -m setup
```