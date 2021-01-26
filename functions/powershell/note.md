# checkout powershell version

```shell script
$PSVersionTable
Get-Host
$Host
```

# help system

```shell script
Update-Help
man Get-Help
help about_Foreach
help about_Array
help "*redirect*"
Get-command –noun process

#  `Show-Command` is a very useful teaching and learning tool.
Show-Command Get-EventLog  # Displays PowerShell command information in a graphical window.
```

# search command & cmdlets

```shell script
Get-Command Help
Get-Command *Command*
```

# get system environment variables

```shell script
Get-help "*env*"
help about_Environment_Variables
Get-ChildItem Env:
Get-Item -Path Env:*
[Environment]::GetEnvironmentVariables()
```

> Why not use single method only to get it?

# get event log

```shell script
Get-EventLog -LogName System -EntryType Error -Source  "Service Control*"
```

# get alias of CommandLet

```shell script
get-alias -Name gal
get-alias -Definition get-alias
```

# test connection

```shell script
Test-Connection github.com
Test-Connection github.com -Count 1
```

# Gets a list of the commands entered during the current session

```shell script
Get-History
h
```

> PS Tips or Knowledge Points:
> 1. '%' is an alias of 'ForEach-Object', '$_' is the current object, such as `Get-Process | ForEach-Object {$_.ProcessName}`
> 2. use `object.GetType()` to get type of variable, such as `(cmdlet).GetType()`, `(Get-Process)[0].gettype()`
> 3. use `object| fl` to get each property of object , `object|select *`, `object|get-member` as well sometimes.
> 4. 'double - colon operator' `::`, The `::` operator is the static member accessor. Whereas the dot operator retrieved instance members, the double-colon operator accesses static members (properties as well as methods) on a class, as is the case with the join method in the example at the end of the last section. The left operand to the static member accessor is required to be a type—either a type literal or an expression returning a type, as you see here: `[string]::join('+',(1,2,3))`.
> 5. object in 'square brackets', `[object]`, such as `[System.Math]` indicates the .NET math class. The :: is the static method operator. For example `[math]::Round($x,2)`

## powershell 过滤字符串

```shell
(quser)| where {$_ -match 'admin'}
(quser) -match 'admin'
```

## powershell 正则表达式分割字符串（like awk）

```shell
[regex]::split(((quser) -match 'admin'), '[ ]+')
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