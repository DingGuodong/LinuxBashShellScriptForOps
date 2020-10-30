# PowerShell 5.1 Scripting Notes

# install Windows Management Framework 5.1
[download .NET Framework](https://dotnet.microsoft.com/download/dotnet-framework/thank-you/net48-offline-installer)
[download](https://www.microsoft.com/en-us/download/details.aspx?id=54616)

> **reboot computer is needed.**

# checkout powershell version
```shell script
$PSVersionTable
Get-Host
$Host
```

[PowerShell Module Browser](https://docs.microsoft.com/en-us/powershell/module/)
[Powershell Scripting Reference](https://docs.microsoft.com/en-us/powershell/module/cimcmdlets/?view=powershell-5.1)

## Enable an account by using the pipeline
[Enable-LocalUser](https://docs.microsoft.com/en-us/powershell/module/microsoft.powershell.localaccounts/enable-localuser?view=powershell-5.1)

```shell script
Get-LocalUser -Name "Administrator" | Enable-LocalUser
```

##  Disable an account by using the pipeline
[Disable-LocalUser](https://docs.microsoft.com/en-us/powershell/module/microsoft.powershell.localaccounts/disable-localuser?view=powershell-5.1)

```shell script
Get-LocalUser Guest | Disable-LocalUser
Get-LocalUser -Name "Administrator" | Disable-LocalUser
```

##  Add members to the Administrators group
[Add-LocalGroupMember](https://docs.microsoft.com/en-us/powershell/module/microsoft.powershell.localaccounts/add-localgroupmember?view=powershell-5.1)

```shell script
Add-LocalGroupMember -Group "Administrators" -Member "Admin02", "MicrosoftAccount\username@Outlook.com", "AzureAD\DavidChew@contoso.com", "CONTOSO\Domain Admins"
```


## Remove members from the Administrators group
[Remove-LocalGroupMember](https://docs.microsoft.com/en-us/powershell/module/microsoft.powershell.localaccounts/remove-localgroupmember?view=powershell-5.1)

```shell script
Remove-LocalGroupMember -Group "Administrators" -Member "Admin02", "MicrosoftAccount\username@Outlook.com", "AzureAD\DavidChew@contoso.com", "CONTOSO\Domain Admins"
```

## Enable WinRM

Server side configuration
```shell script
net start winrm
Get-Service | findstr "WinRM"
Enable-PSRemoting -Force
```

Client side configuration
> 是的，你没看错，就是需要这样，客户端也需要进行此配置
```shell script
net start winrm
Get-Service | findstr "WinRM"
Enable-PSRemoting -Force
winrm enumerate winrm/config/listener
```

## Test WinRM

在使用winrs时可能遇到如下报错，需要将目标计算机添加到 TrustedHosts 配置设置
>Winrs error:WinRM 客户端无法处理该请求。如果身份验证方案与 Kerberos 不同，或者客户端计算机未加入到域中， 则必须使用 HTTPS 传输或者必须将目标计算机添加到 TrustedHosts 配置设置。 使用 winrm.cmd 配置 TrustedHosts。请注意，TrustedHosts 列表中的计算机可能未经过身份验证。 通过运行以下命令可获得有关此内容的更多信息: winrm help config。

>In Windows Workgroup environment, there is a need to add a trust for the server that the client initiate a connection to it by using the command `winrm set winrm/config/client @{TrustedHosts="%servername1%,%servername2%"}`.
>Verity the new settings by using the command `winrm enumerate winrm/config/listener`.

```shell script
# on client node
# or using cmd
# winrm set winrm/config/client @{TrustedHosts="%servername1%,%servername2%"}
winrm set winrm/config/client @{TrustedHosts="192.168.88.29,192.168.88.30"}
winrm get winrm/config/client

# or using powershell
Get-Item WSMan:\localhost\Client\TrustedHosts
Set-Item WSMan:\localhost\Client\TrustedHosts -Value "192.168.88.29"
Set-Item WSMan:\localhost\Client\TrustedHosts -Value "192.168.88.29,192.168.88.30"

winrs -r:http://192.168.88.30:5985 ipconfig /all

```
