# Manage Windows Local Account using WMI(Windows Management Instrumentation)

## get powershell version
```shell script
Get-Host
$PSVersionTable
```

## Discovering objects, properties, and methods
https://docs.microsoft.com/zh-cn/powershell/scripting/learn/ps101/03-discovering-objects?view=powershell-7

```shell script
Get-Service -Name w32time | Get-Member
Get-Service -Name w32time | Get-Member -MemberType Method
Get-Service -Name w32time | Select-Object -Property *
Get-Service -Name w32time | Select-Object -Property Status, Name, DisplayName, ServiceType
Get-Service -Name w32time | Select-Object -Property Status, DisplayName, Can*

```

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

> PS Tips:
> 1. '%' is a alias of 'ForEach-Object', '$_' is the current object, such as `Get-Process | ForEach-Object {$_.ProcessName}`
> 2. use `object.GetType()` to get type of variable, such as `(cmdlet).GetType()`, `(Get-Process)[0].gettype()`
> 3. use `object| fl` to get each property of object , `object|select *`, `object|get-member` as well sometimes.
>

## other references
```
/usr/lib/python3/dist-packages/ansible/modules/windows/win_user.ps1
```
