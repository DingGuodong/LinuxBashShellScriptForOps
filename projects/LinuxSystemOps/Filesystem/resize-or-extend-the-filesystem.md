# Linux磁盘扩容方法总结

how to increase filesystem disk space in Linux

> 注：在不确定可行性之前，注意数据备份，或使用测试环境进行测试，以确保无虞。

## 常见需求

- 在不停机、不重启服务器，或者不影响业务的情况下，实现磁盘扩容，即在线磁盘扩容

- 扩容方法能适用于传统物理实体机也能适用于云计算环境等

## 磁盘扩容是扩容了什么

1. 改变了原有磁盘大小或者磁盘数量【这是手段】

2. 改变了原有磁盘分区大小或增加了文件系统数量【这是方法】

3. 改变了文件系统大小或增加了文件系统【这是目的】

## 磁盘扩容中常见的几种情况：

1. 是物理实体机还是虚拟机
   > 物理实体机通常只能添加本地磁盘，虚拟机则可以允许改变磁盘大小从而扩容原有磁盘
   >
   > 注：一些特殊情况：物理机挂载SAN等的，也可以动态调整磁盘大小
2. 是扩容原有磁盘，还是增加新磁盘
   > 扩充原有磁盘可以改变原有分区或文件系统大小，而增加新磁盘只有在使用LVM的情况下才能改变文件系统大小，否则只是增加了文件系统（通过新增挂载点）数量
3. 使用LVM还是非LVM
   > 使用LVM是实现在线扩容的最佳方式，如果不使用LVM则只有在虚拟机内可以改变原有分区大小，而在物理实体机中只能增加文件系统（通过新增挂载点）数量
   >
   > 原先没有使用LVM，新磁盘也可以使用LVM，方便后续使用
4. 文件系统类型是xfs还是ext4

## 常见的几种磁盘配置和扩容思路：

1. 如果是虚拟机，则可以选择扩容原始磁盘，即不添加新磁盘

2. 如果不是虚拟机或是虚拟机，都可以选择添加新磁盘

3. 使用LVM或没有使用LVM，新磁盘使用LVM

## 收集磁盘和文件系统配置信息

收集什么：

1. 磁盘名称（完整路径），如/dev/sda2，/dev/mapper/centos-root
2. 文件系统类型：是xfs还是ext4

```shell
# 查看文件系统(Filesystem)和挂载点(Mount point)以及文件系统磁盘空间大小等
df -h
# 查看文件系统类型(FS TYPE)
df -Th
lsblk -f
# 查看磁盘信息
# 注：lvm中的lv也被认为是磁盘（Model: Linux device-mapper (linear) (dm)）
fdisk -l
parted -l
```

## 发现新磁盘或更新磁盘信息

对于物理实体机或VMware虚拟化等可以使用如下方法：

```shell
echo 1 > /sys/class/scsi_device/device/rescan  # echo 1 > /sys/class/scsi_device/1\:0\:0\:0/device/rescan
echo 1 > /sys/block/sda/device/rescan

echo "- - -" > /sys/class/scsi_host/host0/scan
echo "- - -" > /sys/class/scsi_host/host1/scan
echo "- - -" > /sys/class/scsi_host/host2/scan
```

> 注：对于云计算环境，如阿里云，上述方法可能不适用，需要通过控制台重新启动实例或重新启动服务器

发现新磁盘或更新磁盘信息，使用`fdisk -l`命令进行确认

## 使用fdisk扩容磁盘分区或初始化新硬盘

扩容磁盘分区

注：也可以使用parted实用程序调整分区大小，参照parted的resizepart子命令。

```shell
# 以扩充磁盘分区/dev/sda2为例
fdisk -l
fdisk /dev/sda
p # 打印分区表
d # 删除分区表，此时磁盘数据并不会丢失，但需要注意，在创建新分区表（n）之前不能保存（w），否则会造成数据丢失
2 # dev/sda2的分区号为2，可以通过p命令查看是哪一个分区号
n # 新建分区表
p # 分区类型为主分区
 # 直接回车是执行默认操作，如选择默认的分区号和扇区号等，具体需要查看fdisk输出

w
```

初始化新硬盘

```shell
fdisk -l
fdisk /dev/sdb
n
p



w
```

> 注：在执行w命令后，fdisk会提示：

```text
WARNING: Re-reading the partition table failed with error 16: Device or resource busy.
The kernel still uses the old table. The new table will be used at
the next reboot or after you run partprobe(8) or kpartx(8)
```

> 此时可以使用`partprobe`来使新分区表生效。

## 通知内核分区表发生变化

用于在fdisk扩容分区容量后，通知操作系统内核分区表已发生变化，请求操作系统重读分区表，从而避免重新启动

```shell
partprobe
```

## lvm扩充dm磁盘空间 - 虚拟化环境下增加原有磁盘空间

```shell
pvresize /dev/sda2  # /dev/sda2是扩容后的磁盘分区设备路径，vg也会自动扩容
lvextend -l +100%FREE /dev/mapper/centos-root
```

> 注：可以使用pvs, pvdisplay, vgs, vgdisplay, lvs, lvdisplay 查看物理卷、卷组、逻辑卷的信息

## lvm扩充dm磁盘空间 - 新增磁盘

先使用fdisk新增磁盘

以新增/dev/sdb1为例

```shell
pvdisplay # pvs
pvcreate /dev/sdb1
pvdisplay

vgdisplay # vgs
vgextend centos /dev/sdb1
vgdisplay

lvdisplay # lvs
#lvextend -L +490G /dev/mapper/centos-root
lvextend -l +100%FREE /dev/mapper/centos-root
lvdisplay 
```

## 扩容文件系统大小

```shell
# 对于xfs文件系统
xfs_growfs  /dev/mapper/centos-root
```

```shell
# 对于ext4文件系统
resize2fs /dev/mapper/centos-root
```

## 最后查看文件系统磁盘空间使用情况

```shell
df -h
```

> 注意：对于非LVM磁盘情况，通过新增磁盘和使用新挂载点增加文件系统时，需要修改/etc/fstab，防止重启后不自动挂载