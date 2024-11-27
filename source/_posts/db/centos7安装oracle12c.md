---
title: linux安装oracle 12c
author: 张一雄
summary: oracle
img: https://pub-b24cf0a8c1f14e9386435977aa464959.r2.dev/img/20230816090833.png
categories:
 - 周边
tags:
 - oracle
---

## 出处

https://blog.csdn.net/weixin_51716058/article/details/134981154

## 	下载

阿里网盘 搜索

oracle12c_linux.zip

## 安装

### 修改配置1

这一步必须有

```sh
# 将主机命名为：sobanoodles1
hostnamectl set-hostname sobanoodles1

# 修改 /etc/hosts 文件 添加如下内容
172.24.228.44   sobanoodles1    sobanoodles1

```

```sh
# oracle12c安装前的环境配置
vim /etc/sysctl.conf
#在最后添加如下内容
# oracle 12c
fs.file-max = 6815744
kernel.sem = 250 32000 100 128
kernel.shmmni = 4096
kernel.shmall = 1073741824
kernel.shmmax = 4398046511104
kernel.panic_on_oops = 1
net.core.rmem_default = 262144
net.core.rmem_max = 4194304
net.core.wmem_default = 262144
net.core.wmem_max = 1048576
net.ipv4.conf.all.rp_filter = 2
net.ipv4.conf.default.rp_filter = 2
fs.aio-max-nr = 1048576
net.ipv4.ip_local_port_range = 9000 65500
```

```sh
sysctl -p
```

### 修改配置2

```sh
vim /etc/security/limits.conf
#在最后添加如下内容

oracle   soft   nofile    1024
oracle   hard   nofile    65536
oracle   soft   nproc    16384
oracle   hard   nproc    16384
oracle   soft   stack    10240
oracle   hard   stack    32768
oracle   hard   memlock    134217728
oracle   soft   memlock    134217728

```

### 安装依赖

```sh
yum install binutils -y \
yum install compat-libcap1 -y \
yum install compat-libstdc++-33 -y \
yum install compat-libstdc++-33.i686 -y \
yum install glibc -y \
yum install glibc.i686 -y \
yum install glibc-devel -y \
yum install glibc-devel.i686 -y \
yum install ksh -y \
yum install libaio -y \
yum install libaio.i686 -y \
yum install libaio-devel -y \
yum install libaio-devel.i686 -y \
yum install libX11 -y \
yum install libX11.i686 -y \
yum install libXau -y \
yum install libXau.i686 -y \
yum install libXi -y \
yum install libXi.i686 -y \
yum install libXtst -y \
yum install libXtst.i686 -y \
yum install libgcc -y \
yum install libgcc.i686 -y \
yum install libstdc++ -y \
yum install libstdc++.i686 -y \
yum install libstdc++-devel -y \
yum install libstdc++-devel.i686 -y \
yum install libxcb -y \
yum install libxcb.i686 -y \
yum install make -y \
yum install nfs-utils -y \
yum install net-tools -y \
yum install smartmontools -y \
yum install sysstat -y \
yum install unixODBC -y \
yum install unixODBC-devel -y
```

### 建立分区

```sh
查看现在分区情况 free -m
如果还没创建交换分区，结果应该swap那一行全是0。

# 建立swap分区
# 创建一个空的 swapfile
install -o root -g root -m 0600 /dev/null /home/swapfile
# 写出一个2gb 的文件名为’/home/swapfile’
dd if=/dev/zero of=/home/swapfile bs=1k count=2048k
# 告诉 linux 这是交换文件:
mkswap /home/swapfile
swapon /home/swapfile`


# 修改 /etc/fstab
vim /etc/fstab
 # 添加下面这行
/home/swapfile swap swap defaults 0 0 
# 上面行的作用是设置为开机自启动


# 查看分区情况 
free -m
# 结果swap那一行结果大小和自己设置的大小一样

```

### 创建用户

```sh
#创建安装oracle12c需要的用户组和用户，oinstall组用于安装数据库，dba组用于管理数据库，-g表示这个用户的主组，-G标识这个用户的其它组
groupadd -g 54321 oinstall 
groupadd -g 54322 dba
groupadd -g 54323 oper
useradd -u 54321 -g oinstall -G dba,oper oracle
# 设置oracle密码：
passwd oracle
# 123456
```

### 设置SELINUX

暂时不设置，感觉没啥用，我设置成了SELINUX=disabled

```sh
#设置SELINUX
vim /etc/selinux/config
#设置内容： 
SELINUX=permissive

```

```sh
setenforce Permissive
```

### 创建oracle目录

```sh
# 创建Oracle安装目录
mkdir -p /usr/local/products/oracle12c
chown -R oracle:oinstall /usr/local
chmod -R 775 /usr/local/

```

### 切换用户

```sh

# 切换到oracle用户
su - oracle
# 进入 oracle用户的根目录下
cd ~
# 查看当前目录下的所有文件，包括隐藏文件
ls -a
#编辑 .bash_profile 文件，并在最后添加如下内容
vim .bash_profile


# cdb1 是表空间名字
export TMP=/tmp
export TMPDIR=$TMP
export ORACLE_HOSTNAME=solang
export ORACLE_UNQNAME=cdb1
export ORACLE_BASE=/usr/local/products
export ORACLE_HOME=$ORACLE_BASE/oracle12c
export ORACLE_SID=cdb1 
export PATH=/usr/sbin:/usr/local/bin:$PATH
export PATH=$ORACLE_HOME/bin:$PATH
export LD_LIBRARY_PATH=$ORACLE_HOME/lib:/lib:/usr/lib
export CLASSPATH=$ORACLE_HOME/jlib:$ORACLE_HOME/rdbms/jlib
```

### 立即生效

```sh
#立即生效
source .bash_profile
echo $ORACLE_HOME

```

### 解压安装包

```sh
# 切换root账号，并将oracle12c压缩包上传到  /home/oracle 目录下
su - root
yum -y install unzip
cd /home/oracle
unzip linuxx64_12201_database.zip
# 删除
rm -rf linuxx64_12201_database.zip
```

### 修改配置

```sh
cd database/response/
vim db_install.rsp
# 编辑的时候可能没有权限（此处已经是root用户了，可进行修改）。
# 解决办法： su 切换到 root用户 对文件授权 chmod -R 775 /home/oracle/database/response/db_install.rsp   #chmod -R 775 绝对路径/文件

#编辑 db_install.rsp，对应修改
oracle.install.option=INSTALL_DB_SWONLY
UNIX_GROUP_NAME=oinstall
INVENTORY_LOCATION=/usr/local/oraInventory
ORACLE_HOME=/usr/local/products/oracle12c
ORACLE_BASE=/usr/local/products
oracle.install.db.InstallEdition=EE
oracle.install.db.OSDBA_GROUP=dba
oracle.install.db.OSBACKUPDBA_GROUP=dba
oracle.install.db.OSDGDBA_GROUP=dba
oracle.install.db.OSKMDBA_GROUP=dba
oracle.install.db.OSRACDBA_GROUP=dba

```

#### 说明

1. oracle.install.option=INSTALL_DB_SWONLY
   - 这个参数指定了安装操作的类型。`INSTALL_DB_SWONLY` 表示仅安装数据库软件，不创建数据库实例。这意味着安装程序将安装Oracle数据库软件到指定的位置，但不会创建数据库或进行数据库的初始化配置。
2. UNIX_GROUP_NAME=oinstall
   - 这个参数指定了安装Oracle软件时所使用的UNIX/Linux操作系统用户组。`oinstall` 组通常用于Oracle软件的安装和管理。该组应该已经存在于系统中，且Oracle安装和运行的用户应该是这个组的成员。
3. INVENTORY_LOCATION=/usr/local/oraInventory
   - 指定Oracle库存（Inventory）的位置。Oracle库存是一个包含所有Oracle安装信息的中心存储库，如安装的组件、补丁和安装路径等。这个位置需要具有足够的空间来存储这些信息，并且应该是可访问的，因为Oracle软件的后续操作（如打补丁）可能需要访问它。
4. ORACLE_HOME=/usr/local/products/oracle12c
   - 指定Oracle软件的安装目录（ORACLE_HOME）。这个目录包含了Oracle数据库软件的二进制文件、库文件、网络配置文件、管理脚本等。这个路径应该是唯一的，避免与其他Oracle软件的安装冲突。
5. ORACLE_BASE=/usr/local/products
   - 指定Oracle数据库的基目录（ORACLE_BASE）。这个目录是Oracle所有产品的根目录，可以包含多个ORACLE_HOME。在Oracle的某些安装中，它用于组织和分隔不同的Oracle安装或版本。
6. oracle.install.db.InstallEdition=EE
   - 指定要安装的Oracle数据库的版本或版本类型。`EE` 代表企业版（Enterprise Edition），是Oracle提供的功能最全面的版本，适用于需要最高性能、可伸缩性、安全性和高级数据库特性的应用。
7. oracle.install.db.OSDBA_GROUP=dba
   - 指定数据库管理员（DBA）所在的操作系统用户组。在这个例子中，它被设置为`dba`。这意味着`dba`组的成员将具有数据库管理权限，能够执行数据库的管理任务。
8. oracle.install.db.OSBACKUPDBA_GROUP=dba
   - 指定备份数据库管理员所在的操作系统用户组。同样设置为`dba`，这意味着这些用户组（在这里是`dba`）的成员将能够执行数据库的备份操作。
9. oracle.install.db.OSDGDBA_GROUP=dba
   - 指定数据卫士（Data Guard）数据库管理员所在的操作系统用户组。Data Guard是Oracle提供的一种高可用性解决方案，允许用户创建一个或多个数据库的实时备份。这里也设置为`dba`。
10. oracle.install.db.OSKMDBA_GROUP=dba
    - 指定知识管理数据库管理员所在的操作系统用户组。这通常与Oracle企业管理器（Enterprise Manager）或数据库管理相关的特定功能相关，但也设置为`dba`。
11. oracle.install.db.OSRACDBA_GROUP=dba
    - 指定RAC（Real Application Clusters）数据库管理员所在的操作系统用户组。RAC是Oracle提供的一种高可用性和可扩展性的数据库解决方案，允许多个实例在多个节点上同时访问同一个数据库。这里也设置为`dba`。

### 安装

```sh
# 在oracle用户下操作
su - oracle 
cd ~/database
#静默安装oracle12c(不可用)
./runInstaller -ignoreSysPrereqs -ignorePrereq -waitforesponseFile /home/oracle/database/response/db_install.rsp
# 或者（执行的是下面这个）（可用）
./runInstaller -ignoreSysPrereqs -ignorePrereq -waitforcompletion \ -showProgress -silent -responseFile /home/oracle/database/response/db_install.rsp
```

```sh
# 切换到root用户
su root
/usr/local/oraInventory/orainstRoot.sh
/usr/local/products/oracle12c/root.sh
```

### 测试是否安装成功

```sh
# oracle数据库软件安装成功
su - oracle
sqlplus / as sysdba

# 退出
exit
```

### 创建数据库(公司看下面的配置)

此处需要修改 sid（表空间名称），存放路径(怎么修改？) ，账户密码、字符集（ZHS16GBK）  等等注意修改！

cdb1 是上面配置的表空间，一定要一致，否则不好使

```sh
# 数据库创建，使用数据库配置助手DBCA静默模式下创建数据库
dbca -silent -createDatabase \
 -templateName /usr/local/products/oracle12c/assistants/dbca/templates/General_Purpose.dbc \
 -gdbname cdb1 -sid cdb1 -responseFile /home/oracle/database/response/dbca.rsp \
 -characterSet AL32UTF8 \
 -sysPassword OraPasswd1 \
 -systemPassword OraPasswd1 \
 -createAsContainerDatabase true \
 -numberOfPDBs 1 \
 -pdbName pdb1 \
 -pdbAdminPassword OraPasswd1 \
 -automaticMemoryManagement false \
 -ignorePreReqs
```

#### 公司

新增时 需要修改gdbname、sid、pdbName，其他的不用修改

```sh
# 数据库创建，使用数据库配置助手DBCA静默模式下创建数据库
dbca -silent -createDatabase \
 -templateName /usr/local/products/oracle12c/assistants/dbca/templates/General_Purpose.dbc \
 -gdbname cdb1 -sid cdb1 -responseFile /home/oracle/database/response/dbca.rsp \
 -characterSet ZHS16GBK \
 -sysPassword OraPasswd1 \
 -systemPassword OraPasswd1 \
 -createAsContainerDatabase true \
 -numberOfPDBs 1 \
 -pdbName pdb1 \
 -pdbAdminPassword OraPasswd1 \
 -automaticMemoryManagement false \
 -ignorePreReqs
```



#### 说明

- `dbca -silent -createDatabase`：这是调用DBCA命令的基本格式，`-silent`指定了静默模式，`-createDatabase`表示要进行数据库创建操作。
- `-templateName /usr/local/products/oracle12c/assistants/dbca/templates/General_Purpose.dbc`：指定用于创建数据库的模板文件路径。这里使用的是一般用途（General_Purpose）的模板，它预定义了一些配置选项，适合大多数用途。
- `-gdbname cdb1`：设置全局数据库名（Global Database Name）为`cdb1`。在多租户架构中，这是CDB（容器数据库）的名称。
- `-sid cdb1`：设置系统标识符（System Identifier）为`cdb1`。在某些上下文中，这也可以被理解为数据库的唯一名称或实例名。
- `-responseFile /home/oracle/database/response/dbca.rsp`：指定包含额外配置选项的响应文件路径。这个文件允许你预定义更多的配置参数，这些参数在命令行中没有直接指定。
- `-characterSet AL32UTF8`：设置数据库的字符集为`AL32UTF8`，这是一个支持多种语言的Unicode字符集。
- `-sysPassword OraPasswd1`：设置SYS用户的密码为`OraPasswd1`。SYS是Oracle数据库中权限最高的用户之一。
- `-systemPassword OraPasswd1`：设置SYSTEM用户的密码为`OraPasswd1`。SYSTEM用户是Oracle数据库中另一个重要的管理员账户。
- `-createAsContainerDatabase true`：指定创建的数据库应该是一个容器数据库（CDB），这在Oracle 12c及更高版本中支持多租户架构。
- `-numberOfPDBs 1`：指定要创建的PDB（可插拔数据库）的数量为1。PDB是CDB中的一个独立数据库，可以插拔。
- `-pdbName pdb1`：设置PDB的名称为`pdb1`。
- `-pdbAdminPassword OraPasswd1`：设置PDB管理员的密码为`OraPasswd1`。注意，这个参数可能不是所有版本的DBCA都支持，具体取决于Oracle的版本和配置。
- `-automaticMemoryManagement false`：禁用自动内存管理。如果设置为`true`，Oracle将自动管理数据库的SGA和PGA内存大小。设置为`false`允许你手动设置这些值。
- `-ignorePreReqs`：忽略先决条件检查。这可能会让DBCA忽略一些错误或警告，这些错误或警告原本可能会阻止数据库的创建。使用此选项时要小心，因为它可能会导致数据库在不符合要求的环境中运行。

### 测试是否成功

```sh
sqlplus / as sysdba
select status from v$instance; 
# 如图数据库创建成功
```

![image-20240906154821556](https://pub-b24cf0a8c1f14e9386435977aa464959.r2.dev/img/image-20240906154821556.png)

## 配置监听

配置监听第一遍会失败，不知道为什么，但是同样命令执行第二次就成功了！

```sh
#配置监听，使用默认的netca.rsp文件
netca -silent -responseFile /home/oracle/database/response/netca.rsp
```

![image-20240906154947110](https://pub-b24cf0a8c1f14e9386435977aa464959.r2.dev/img/image-20240906154947110.png)

### 修改端口

```sh
# 修改为本机的主机名和oracle对应端口1521
# su 切换到root，授权listener.ora
su - root
chmod -R 775 /usr/local/products/oracle12c/network/admin/listener.ora
su - oracle
vim /usr/local/products/oracle12c/network/admin/listener.ora
lsnrctl status
# 启动和关闭监听
lsnrctl start
lsnrctl stop
```

将localhost改成0.0.0.0 则外网可以访问

![image-20240906155539811](https://pub-b24cf0a8c1f14e9386435977aa464959.r2.dev/img/image-20240906155539811.png)

## 远程链接

```sh
lsnrctl stop && lsnrctl start
```

![image-20240906161337686](https://pub-b24cf0a8c1f14e9386435977aa464959.r2.dev/img/image-20240906161337686.png)

## 开机自动启动

```sh
# 设置开机自启功能：
# 将N修改为Y
vim /etc/oratab
```

下面的不知道是在干嘛

```sh
# 切换root账号，编辑 /etc/init.d/dbora 文件，这个文件应该是不存在的，直接编辑就好。
su root
vim /etc/init.d/dbora
# 内容如下
#! /bin/sh
# description: Oracle auto start-stop script.
#
# Set ORACLE_HOME to be equivalent to the $ORACLE_HOME
# from which you wish to execute dbstart and dbshut;
#
# Set ORA_OWNER to the user id of the owner of the
# Oracle database in ORACLE_HOME.
ORACLE_HOME=/usr/local/products/oracle12c
ORA_OWNER=oracle
case "$1" in
'start') 
    # Start the Oracle databases:
    # The following command assumes that the oracle login
    # will not prompt the user for any values
    # Remove "&" if you don't want startup as a background process.
    su - $ORA_OWNER -c "$ORA_HOME/bin/dbstart $ORA_HOME" &
    touch /var/lock/subsys/dbora
    ;;
'stop')
    # Stop the Oracle databases:
    # The following command assumes that the oracle login
    # will not prompt the user for any values
    su - $ORA_OWNER -c "$ORACLE_HOME/bin/dbshut $ORACLE_HOME" &
    rm -f /var/lock/subsys/dbora
    ;;
esac
```

### 修改用户

```sh
vim /etc/oratab
export ORA_OWNER=oracle
echo $ORA_OWNER     #ORA_OWNER设置为oracle用户
```

### 修改权限

```sh
# 修改dbora组和文件权限
chgrp dba /etc/init.d/dbora
chmod 750 /etc/init.d/dbora

# 创建符号链接
ln -s /etc/init.d/dbora /etc/rc.d/rc0.d/K01dbora
ln -s /etc/init.d/dbora /etc/rc.d/rc3.d/S99dbora
ln -s /etc/init.d/dbora /etc/rc.d/rc5.d/S99dbora

# Oracle数据库开机自动启动，在oracle用户中单独启动和关闭数据库
$ORACLE_HOME/bin/dbstart $ORACLE_HOME
$ORACLE_HOME/bin/dbshut $ORACLE_HOME

```

## 卸载

```sh
find / -name deinstall
su - oracle
lsnrctl stop
cd 路径
./deinstall
```

