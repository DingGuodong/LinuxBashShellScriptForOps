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
