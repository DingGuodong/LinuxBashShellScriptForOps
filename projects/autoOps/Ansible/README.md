# Control Machine Requirements
[Control Machine Requirements](http://docs.ansible.com/ansible/intro_installation.html#control-machine-requirements)

Currently Ansible can be run from any machine with Python 2.6 or 2.7 installed 
(Windows isn't supported for the control machine).

## Install Latest Releases Via Pip
Ansible can be installed via “pip”, the Python package manager. 
If ‘pip’ isn’t already available in your version of Python, you can get pip by:
```bash
$ sudo easy_install pip
```

Then install Ansible with:
```bash
$ sudo pip install ansible
```
Usually, it will install packages:
```text
ansible 
paramiko 
jinja2 
pycrypto 
pyasn1 
cryptography 
MarkupSafe 
idna 
asn1crypto 
packaging 
cffi 
pyparsing 
pycparser
```

Or if you are looking for the latest development version:
```bash
pip install git+git://github.com/ansible/ansible.git@devel
```
Readers that use virtualenv can also install Ansible under virtualenv, 
though we’d recommend to not worry about it and just install Ansible globally. 
Do not use easy_install to install ansible directly.


