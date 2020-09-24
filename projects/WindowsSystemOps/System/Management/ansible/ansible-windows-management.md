# Ansible manage Microsoft Windows hosts

[Windows Guides](https://docs.ansible.com/ansible/latest/user_guide/windows.html)

[Host Requirements](https://docs.ansible.com/ansible/latest/user_guide/windows_setup.html#host-requirements)

[Authentication Options](https://docs.ansible.com/ansible/latest/user_guide/windows_winrm.html#authentication-options)

>Upgrading PowerShell and .NET Framework(reboot is required)
>
>Ansible requires PowerShell version 3.0 and .NET Framework 4.0 or newer to function on older operating systems like Server 2008 and Windows 7.
> 
>[Windows Management Framework 3.0](https://www.microsoft.com/en-us/download/details.aspx?id=34595)
>
>[the Upgrade-PowerShell.ps1 script](https://raw.githubusercontent.com/jborean93/ansible-windows/master/scripts/Upgrade-PowerShell.ps1)

Setting up a Windows Host

```cmd
winrm quickconfig -q
winrm set winrm/config/service @{AllowUnencrypted="true"}
winrm get winrm/config/Service
winrm get winrm/config/Winrs
```

>Tips: use NTLM for both Local Accounts and Active Directory Accounts

```yaml
[localwindows]
dc1.example.com ansible_user='chris.ding@example.com' ansible_password="plaintext_password" ansible_port=5985 ansible_connection="winrm" ansible_winrm_transport=kerberos ansible_winrm_server_cert_validation=ignore
192.168.88.38   ansible_user='chris.ding' ansible_password="plaintext_password"  ansible_port=5985 ansible_connection="winrm" ansible_winrm_transport=ntlm ansible_winrm_server_cert_validation=ignore
```

### using Kerberos auth
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

### check Kerberos auth result
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

### FAQ

Q: "msg": "kerberos: Bad HTTP response returned from server. Code 500, plaintext: the specified credentials were rejected by the server"
A: make WinRM accept unencrypted communication with a client.

https://stackoverflow.com/questions/39905667/kerberos-authentication-over-http-failing-with-ansible-playbook

https://github.com/diyan/pywinrm/

```shell script
winrm get winrm/config/service
winrm set winrm/config @{AllowUnencrypted="true"}
winrm set winrm/config/service @{AllowUnencrypted="true"}  # alternative 

```

```powershell
Set-Item -Path "WSMan:\localhost\Service\AllowUnencrypted" -Value $true
Set-Item -Path WSMan:\localhost\Service\AllowUnencrypted -Value $true  # alternative 
```

note: sometimes, system anti-virus program, such as 360, will deny ansible access system.
```text
[WARNING]: ERROR DURING WINRM SEND INPUT - attempting to recover: WinRMError 管道正在被关闭。  (extended fault data: {'transport_message':
'Bad HTTP response returned from server. Code 500', 'http_status_code': 500, 'wsmanfault_code': '232', 'fault_code': 's:Receiver',
'fault_subcode': 'w:InternalError'})
192.168.88.132 | FAILED! => {
    "msg": "winrm send_input failed; \nstdout: \nstderr Access is denied.\r\n"
}

[WARNING]: ERROR DURING WINRM SEND INPUT - attempting to recover: WinRMOperationTimeoutError
192.168.88.132 | FAILED! => {
    "msg": "winrm send_input failed; \nstdout: \nstderr Access is denied.\r\n"
}
```

Q: "msg": "kerberos: the specified credentials were rejected by the server",
A: no ans so far