# ansible manage Windows Server in Active Directory

## using Kerberos auth
sudo apt install krb5-user  # user will be asked input a default_realm, such as 'EXAMPLE.COM'

cat /etc/krb5.conf
```text
[libdefaults]
	default_realm = EXAMPLE.COM

	kdc_timesync = 1
	ccache_type = 4
	forwardable = true
	proxiable = true
[realms]
	EXAMPLE.COM = {
		kdc = EXAMPLE.COM
		admin_server = EXAMPLE.COM
	}

[domain_realm]
	.e-bao.cn = EXAMPLE.COM
	e-bao.cn = EXAMPLE.COM
```
kinit Chris.Ding@EXAMPLE.COM

## check Kerberos auth result
kinit -C chris.ding@example.com # username here is case insensitive
klist


ansible-vault create groups_vars/localwindows.yml
ansible-vault edit groups_vars/localwindows.yml
```yaml
ansible_user: chris.ding@EXAMPLE.COM
ansible_password: plaintext_password
ansible_port: 5985
ansible_connection: winrm
ansible_winrm_server_cert_validation: ignore
```

ansible -i hosts localwindows -m win_ping --ask-vault-pass -e @groups_vars/localwindows.yml
```ini
[localwindows]
dc1.example.com
dc2.example.com
```

## FAQ

Q: "msg": "kerberos: Bad HTTP response returned from server. Code 500, plaintext: the specified credentials were rejected by the server"
A: make WinRM accept unencrypted communication with a client.

https://stackoverflow.com/questions/39905667/kerberos-authentication-over-http-failing-with-ansible-playbook

https://github.com/diyan/pywinrm/

```shell script
winrm get winrm/config/service
winrm set winrm/config @{AllowUnencrypted="true"}
```

```powershell
Set-Item -Path "WSMan:\localhost\Service\AllowUnencrypted" -Value $true
```