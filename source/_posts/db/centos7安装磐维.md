---
title: centos7安装磐维数据库
img: https://pub-b24cf0a8c1f14e9386435977aa464959.r2.dev/img/bttp.png
categories:
 - 数据库
tags:
 - 磐维
 - coenos7
---

## 配置

### 创建文件夹

```sh
mkdir -p /database/panweidb/data \
mkdir -p /database/panweidb/data/pg_xlog \
mkdir -p /database/panweidb/log \
mkdir -p /database/panweidb/pg_audit \
mkdir -p /database/panweidb/app \
mkdir -p /database/panweidb/cm \
mkdir -p /database/panweidb/soft \
mkdir -p /backup \
mkdir -p /archive
```

### 修改root可登录

```sh
cat /etc/ssh/sshd_config | grep PermitRootLogin
PermitRootLogin yes
vi /etc/ssh/sshd_config

# 重启sshd服务
systemctl restart sshd
```

### 关闭SELINUX

```sh
# 修改配置文件
cat /etc/selinux/config | grep -i SELINUX
SELINUX=disabled

# 关闭SELINUX 执行⬇️
setenforce 0
```

### 关闭防火墙

```sh
# 查看防火墙状态
systemctl status firewalld

# 关闭防火墙
systemctl disable firewalld.service
systemctl stop firewalld.servic
```

### 设置字符集

```sh
# 查看字符集
echo $LANG
# 设置字符集
export LANG=en_US.UTF-8
```

### 关闭 swap 交换

```sh
swapoff -a
```

### 设置网卡MTU值

略过不做

### 关闭THP

```sh
#检查THP开启情况
cat /sys/kernel/mm/transparent_hugepage/enabled
always madvise [never]

##关闭THP
echo never > /sys/kernel/mm/transparent_hugepage/enabled
## 设置重启后自动关闭
chmod +x /etc/rc.d/rc.local
systemctl enable rc-local.service

cat >> /etc/rc.d/rc.local <<EOF
swapoff -a
if test -f /sys/kernel/mm/transparent_hugepage/enabled;
then
   echo never > /sys/kernel/mm/transparent_hugepage/enabled
fi
if test -f /sys/kernel/mm/transparent_hugepage/defrag;
then
  echo never > /sys/kernel/mm/transparent_hugepage/defrag
fi
EOF
```

### 关闭RemoveIPC

```sh
 (1) 修改/etc/systemd/logind.conf文件中的“RemoveIPC”值为“no”
vim  /etc/systemd/logind.conf
RemoveIPC=no

(2) 修改/usr/lib/systemd/system/systemd-logind.service文件中的“RemoveIPC”值为“no”
vim /usr/lib/systemd/system/systemd-logind.service
RemoveIPC=no

(3) 重启服务
systemctl daemon-reload
systemctl restart systemd-logind.service

(4) 结果验证确认
loginctl show-session | grep RemoveIPC
systemctl show systemd-logind | grep RemoveIPC
```

### 内核参数优化

```sh
vi /etc/sysctl.conf

# panweidb
net.ipv4.tcp_max_tw_buckets = 10000
net.ipv4.tcp_tw_reuse = 1 
net.ipv4.tcp_keepalive_time = 30
net.ipv4.tcp_keepalive_probes = 9
net.ipv4.tcp_keepalive_intvl = 30
net.ipv4.tcp_retries1 = 5
net.ipv4.tcp_syn_retries = 5
net.ipv4.tcp_synack_retries = 5
net.ipv4.tcp_retries2 = 12
vm.overcommit_memory = 0
net.ipv4.tcp_rmem = 8192 250000 16777216
net.ipv4.tcp_wmem = 8192 250000 16777216
net.core.wmem_max = 21299200
net.core.rmem_max = 21299200
net.core.wmem_default = 21299200
net.core.rmem_default = 21299200
net.ipv4.ip_local_port_range = 26000 65535
kernel.sem = 250 6400000 1000 25600
net.core.somaxconn = 65535
net.ipv4.tcp_syncookies = 1
net.core.netdev_max_backlog = 65535
net.ipv4.tcp_max_syn_backlog = 65535
net.ipv4.tcp_fin_timeout = 60
kernel.shmall = 1073741824 
kernel.shmmax = 751619276800 
net.ipv4.tcp_sack = 1
net.ipv4.tcp_timestamps = 1
vm.extfrag_threshold = 500
vm.overcommit_ratio = 90
vm.swappiness = 0

# 生效
sysctl -p
```

### 3.11 配置资源限制

```sh
vi /etc/security/90-nproc.conf
或者
vi /etc/security/limits.conf
```

```sh
# panweidb
* soft nofile 1000000
* hard nofile 1000000
* soft nproc 655360
* hard nproc 655360
* soft memlock unlimited
* hard memlock unlimited
* soft core unlimited
* hard core unlimited
* soft stack unlimited
* hard stack unlimited
```

## 安装

### 安装依赖

```sh
yum -y install libaio-devel flex bison ncurses-devel glibc-devel patch readline-devel python3 expect* bzip2 libnsl gcc gcc-c++ zlib-devel ncurses-devel expect
```

### 修改用户名

```sh
# 用localhost会报错
cat >> /etc/hosts <<-ROF
192.168.159.128 hostname1
ROF

# 修改
hostnamectl set-hostname hostname1
# 查看
```



### 创建用户

```sh
groupadd -g 1101 dbgrp
useradd -g dbgrp -u 1101 -m omm
passwd omm
(omm密码：123456)
```

### 创建目录

```sh
mkdir -p /database/panweidb \
mkdir -p /database/panweidb/archive \
mkdir -p /database/panweidb/pg_audit

mkdir -p /database/panweidb/soft
```

### 解压安装包

```sh\
# 将安装包存放在/database/panweidb/soft 目录下
cd /database/panweidb/soft

#BCLinux 8.2 x86
tar -xf 'PanWeiDB-2.0.0_Build0(03b85d1)-bclinux_8.2-x86_64-no_mot.tar.gz'
tar -xf 'PanWeiDB-2.0.0_Build0(03b85d1)-bclinux-64bit-om.tar.gz'

#BCLinux For Euler 21.10 x86
tar -xf 'PanWeiDB-2.0.0_Build0(03b85d1)-bclinux_euler21.10-x86_64-no_mot.tar'
tar -xf 'PanWeiDB-2.0.0_Build0(03b85d1)-bclinux-64bit-om.tar.gz'

#其他操作系统类似
```

### 编写XML文件(主节点)

### 配置节点

```sh
vim /database/panweidb/soft/panweidb1m.xml
# 用localhost会报错,所以需要写死ip地址，不知道用127.0.0.1行不行
```

```xml
<?xml version="1.0" encoding="utf-8"?>
<ROOT>
  <CLUSTER>
    <PARAM name="clusterName" value="panweidb" />
    <PARAM name="nodeNames" value="hostname1"/>
    <PARAM name="gaussdbAppPath" value="/database/panweidb/app" />
    <PARAM name="gaussdbLogPath" value="/database/panweidb/log" />
    <PARAM name="tmpMppdbPath" value="/database/panweidb/tmp"/>
    <PARAM name="gaussdbToolPath" value="/database/panweidb/tool" />
    <PARAM name="corePath" value="/database/panweidb/corefile"/>
    <PARAM name="backIp1s" value="192.168.159.128"/>
  </CLUSTER>
  
  <DEVICELIST>
    <DEVICE sn="hostname1">
      <PARAM name="name" value="hostname1"/>
      <PARAM name="azName" value="AZ1"/>
      <PARAM name="azPriority" value="1"/>
      <PARAM name="backIp1" value="192.168.159.128"/>
      <PARAM name="sshIp1" value="192.168.159.128"/>
      <PARAM name="dataNum" value="1"/>
      <PARAM name="dataPortBase" value="17700"/>
      <PARAM name="dataNode1" value="/database/panweidb/data"/>
    </DEVICE>
  </DEVICELIST>
</ROOT>
```

### 安装目录授权

```sh
chown -R omm:dbgrp /database/panweidb 
chmod -R 755 /database/panweidb
```

### 预安装

```sh
cd /database/panweidb/soft/script
tar -zxvf PanWeiDB-2.0.0_Build0\(9fbca90\)-CentOS-64bit-om.tar.gz
tar -zxvf PanWeiDB-2.0.0_Build0\(9fbca90\)-centos_7-x86_64-no_mot.tar.gz 
cd /database/panweidb/soft/script
#单节点
./gs_preinstall -U omm -G dbgrp -X /database/panweidb/soft/panweidb1m.xml

#两节点：一主一备
./gs_preinstall -U omm -G dbgrp -X /database/panweidb/soft/panweidb1m1s.xml

#三节点：一主两备
./gs_preinstall -U omm -G dbgrp -X /database/panweidb/soft/panweidb1m2s.xml
```

## 继续安装

### 授权

```sh
chown -R omm:dbgrp /database/panweidb
chmod -R 755 /database/panweidb
```

### omm用户安装(主节点)

输入的密码 必须是8位以上 包含三种字符

密码：Xiong1991

```sh
su - omm
cd /database/panweidb/soft/script

#单节点
# dbcompatibility=A 为兼容oracle
gs_install -X /database/panweidb/soft/panweidb1m.xml \
--gsinit-parameter="--encoding=UTF8" \
--gsinit-parameter="--lc-collate=C" \
--gsinit-parameter="--lc-ctype=C" \
--gsinit-parameter="--dbcompatibility=A"

#两节点：一主一备
gs_install -X /database/panweidb/soft/panweidb1m1s.xml \
--gsinit-parameter="--encoding=UTF8" \
--gsinit-parameter="--lc-collate=C" \
--gsinit-parameter="--lc-ctype=C" \
--gsinit-parameter="--dbcompatibility=PG"

#三节点：一主两备
gs_install -X /database/panweidb/soft/panweidb1m2s.xml \
--gsinit-parameter="--encoding=UTF8" \
--gsinit-parameter="--lc-collate=C" \
--gsinit-parameter="--lc-ctype=C" \
--gsinit-parameter="--dbcompatibility=B"
```

### 设置最大内存

```sh
gs_guc set -N all -c "max_process_memory=6000MB"
```

## 使用

### 登录

```sh
 # 登录客户端
 gsql -U omm -r
 
 gsql -U omm -d panweidb -p 17700 -h localhost

 # 查询
 select * from pg_user_mapping;
 # 退出
 \q
```

### 重启

```sh
gs_om -t stop && gs_om -t start
```

### 修改外网访问

```sh
/database/panweidb/data
vim postgresql.conf
```

修改

```sh
password_encryption_type = 1
listen_addresses = '*'
```

继续

```sh
cd /database/panweidb/data
vim pg_hba.conf
```

放开（好像默认已经放开了）

```
host    all             all             10.1.161.184/32         sha256
```

重启

```sh
gs_om -t stop && gs_om -t start
```

```sh
jdbc:postgresql://[{host::localhost}[:{port::5432}]]/[{database:database/[^?]+:postgres::%}?][\?<&,user={user:param},password={password:param},{:identifier}={:param}>]
```

### 外部链接

#### 添加白名单

```sh
gs_guc reload -N all -I all -h 'host all all 192.168.100.0/24 sha256'

gs_guc reload -N all -I all -h 'host all all 192.168.1.60/24 sha256'
```

#### 创建新用户

**omm用户不能直接登录**

```sql
gsql -U omm -r
create user testuser with sysadmin  IDENTIFIED BY 'Panwei2024';

gsql -U testuser -d panweidb -p 17700 -h localhost
```

#### 远程链接

新建驱动

![image-20240904095800848](https://pub-b24cf0a8c1f14e9386435977aa464959.r2.dev/img/image-20240904095800848.png)

创建链接

```txt
jdbc:panweidb://192.168.159.128:17700/panweidb
```

![image-20240904095834791](https://pub-b24cf0a8c1f14e9386435977aa464959.r2.dev/img/image-20240904095834791.png)

#### 报错

```txt
[0A000][9684] org.panweidb.util.PSQLException: ERROR: units "epoch" not supported 在位置：referenced column: startup_time.
```

![image-20240904095918040](https://pub-b24cf0a8c1f14e9386435977aa464959.r2.dev/img/image-20240904095918040.png)
