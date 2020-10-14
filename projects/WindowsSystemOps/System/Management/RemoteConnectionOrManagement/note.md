# PowerShell 5.1 Scripting Notes

# install Windows Management Framework 5.1
[download .NET Framework](https://dotnet.microsoft.com/download/dotnet-framework/thank-you/net48-offline-installer)
[download](https://www.microsoft.com/en-us/download/details.aspx?id=54616)

> **reboot computer is needed.**

# checkout powershell version
```shell script
Get-Host
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