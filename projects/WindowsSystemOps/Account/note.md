# Manage Windows Local Account using WMI(Windows Management Instrumentation)

## get and set user account

```shell script
wmic useraccount /?
wmic useraccount where "LocalAccount=true" get name
wmic useraccount where 'Disabled=false' get fullname

wmic useraccount where 'LocalAccount=true and Name="guodong"' get Disabled
wmic useraccount where 'LocalAccount=true and Name="guodong"' set Disabled=True
wmic useraccount where 'LocalAccount=true and Name="guodong"' set Disabled=False
```

```shell script
Get-WmiObject Win32_UserAccount -filter 'LocalAccount=True AND Name="guodong"'
Get-WmiObject Win32_UserAccount -filter "LocalAccount=True AND Name=`"guodong`""

Get-WmiObject Win32_UserAccount -filter 'LocalAccount=True AND Name="guodong"'|Select-Object -Property Disabled
(Get-WmiObject Win32_UserAccount -filter 'LocalAccount=True AND Name="guodong"').Disabled


# (Get-WmiObject Win32_UserAccount -filter 'LocalAccount=True AND Name="guodong"').gettype()
# note: .put() operation need administrator privilege
Get-WmiObject Win32_UserAccount -filter 'LocalAccount=True AND Name="guodong"' | % {$_.Disabled = $false;$_.put()}
Get-WmiObject Win32_UserAccount -filter 'LocalAccount=True AND Name="guodong"' | % {$_.Disabled = $true;$_.put()}
```

> ManagementObject.Put Method: ManagementObject.Put()
> Google: 'ManagementObject put site:microsoft.com'
> https://docs.microsoft.com/zh-cn/dotnet/api/system.management.managementobject.put?view=dotnet-plat-ext-3.1
> https://docs.microsoft.com/en-us/dotnet/api/system.management.managementobject.put?view=dotnet-plat-ext-3.1

## other references

```
/usr/lib/python3/dist-packages/ansible/modules/windows/win_user.ps1
```

## use `NET USER` command to manage user accounts

```shell script
# disable user account
NET USER <username> /ACTIVE:NO
# enable user account
NET USER <username> /ACTIVE:YES
```

## get user's groups

```shell
net user <username>
[System.Security.Principal.WindowsIdentity]::GetCurrent().Groups | ForEach-Object { $_.Translate([System.Security.Principal.NTAccount]).Value } | Sort-Object
```