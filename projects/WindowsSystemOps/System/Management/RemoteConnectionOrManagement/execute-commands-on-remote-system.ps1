# 利用WinRM和Invoke-Command等在客户端上运行服务器上的命令或上传下载文件
# Run the command on remote server with PowerShell
# 参考：
#   http://2mysite.net/archives/powershell-远程执行任务/
#   http://2mysite.net/archives/powershell-%E8%BF%9C%E7%A8%8B%E6%89%A7%E8%A1%8C%E4%BB%BB%E5%8A%A1/
#
# 注意：客户端与服务端均需要开启WinRM服务，且需要以管理员权限运行此脚本或脚本内容
Start-Service WinRM  # 确保本地开启WinRM服务
Get-Service WinRM
Test-WsMan  # 前提：开启WinRM服务

# 配置远程服务器信息和用户登录凭据
$COMPUTER_NAME="192.168.88.30"  # 填写服务器名称（需可解析）或IP，如果有多个服务器地址，可以用逗号隔开
$USERNAME = 'name@example.xom' # 支持域（xxx\xxx.xxx或xxx.xxx@xxx）和工作站等账户
$PASSWORD = 'secret'

# 测试远程服务器WinRM是否可用, Tests whether the WinRM service is running on a local or remote computer.
Test-WsMan $COMPUTER_NAME

# 添加远程服务器到本地信任
Get-Item WSMan:\localhost\Client\TrustedHosts
Set-Item WSMan:\localhost\Client\TrustedHosts -Value $COMPUTER_NAME -Concatenate
Get-Item WSMan:\localhost\Client\TrustedHosts

# 生成远程服务器PS专用登录凭据
$PASS = ConvertTo-SecureString -AsPlainText $PASSWORD -Force
$CREDENTIAL = New-Object System.Management.Automation.PSCredential -ArgumentList $USERNAME,$PASS

# 创建PSSession以便执行多个命令或用于上传下载
$s = New-PSSession -ComputerName $COMPUTER_NAME

# （可选）查看PSSession对象属性
$s|Get-Member

# （可选）选择合适的PSSession
Get-PSSession -ComputerName $COMPUTER_NAME -State Opened

# 开始执行多个命令（PSSession支持上下文，所以命令之间可以存在联系（如可共享变量等））
Invoke-Command -Session $s -ScriptBlock {$p = Get-Process PowerShell}
Invoke-Command -Session $s -ScriptBlock {$p.VirtualMemorySize}

# 在PowerShell里运行cmd命令（非PS命令）
Invoke-Command -Session $s -ScriptBlock {ipconfig; echo 1}

# 本地上传文件到服务器
Copy-Item -Path .\task.ps1 -Destination C:\task.ps1 -ToSession $s
Copy-Item -Path C:\PowerShell -Destination F:\temp -ToSession $s -Recurse

# 从服务器下载文件到本地
Copy-Item -Path C:\task.ps1 -Destination F:\temp\task.ps1 -FromSession $s
Copy-Item -Path C:\PowerShell -Destination F:\temp -FromSession $s -Recurse

# 关闭PSSession
$s | Remove-PSSession
Get-PSSession | Remove-PSSession