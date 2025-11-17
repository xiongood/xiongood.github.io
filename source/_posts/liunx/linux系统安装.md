---
title: CentOS7系统安装
summary: centos7的安装以及网络的配置
categories:
 - linux
tags:
 - linux
 - VMware
---

## 下载地址

下载 ：CentOS-7-x86_64-Minimal-2009.iso

### 华为下载源

```http
https://repo.huaweicloud.com/centos/
```

```http
https://repo.huaweicloud.com/centos/7.9.2009/isos/x86_64/
```

![image-20230421095147566](https://img.myfox.fun/img/20230421095148.png)

### 阿里下载源

```http
https://mirrors.aliyun.com/centos/
```

## 安装

略……

## 配置

### 没有IP

![image-20230419111252942](https://img.myfox.fun/img/image-20230419111252942.png)

- 修改配置文件

```sh
vi /etc/sysconfig/network-scripts/ifcfg-ens33
```

![image-20230419111308767](https://img.myfox.fun/img/image-20230419111308767.png)

- 重启网络

```sh
systemctl restart network
ip addr
```

![image-20230419111318355](https://img.myfox.fun/img/image-20230419111318355.png)

- 关闭虚拟机，设置网络连接模式

![image-20230419111326030](https://img.myfox.fun/img/image-20230419111326030.png)

### ping 不通百度

#### 修改dns

```sh
vi /etc/resolv.conf
```

```txt
nameserver 223.5.5.5  # 阿里云DNS（国内速度快、稳定）
nameserver 8.8.8.8    # 谷歌DNS（备用，避免单一DNS失效）
```

```sh
ping www.baidu.com
```

#### 修改网络策略

NAT 模式虽然可以简单的链接上互联网，但是有两个问题，1、虚拟机ping不通主机；2、其他局域网机器ping不通虚拟机，只能单机玩，完整版的网络，可以用桥接模式，下面有记录⬇️

![image-20240828170513587](https://img.myfox.fun/img/image-20240828170513587.png)

编辑》虚拟机网络配置器

![image-20240828170539134](https://img.myfox.fun/img/image-20240828170539134.png)

### 关闭防火墙

```sh
#这个亲测可用
systemctl stop firewalld.service
#开机禁止启动
systemctl disable firewalld.service
```

### 安装软件

安装不上的话 看下面的配置阿里yum源

```sh
# 安装ifconfig
yum update -y

yum install net-tools -y\
yum install vim	-y\
yum install wget -y\
yum install unzip -y
# yum install tar
```

![image-20230419111336458](https://img.myfox.fun/img/image-20230419111336458.png)

之后可以通过 xshell 进行链接

### 配置阿里yum源

```sh
#1 备份现有的yum源
cd /etc/yum.repos.d/
mkdir bak
mv *.repo /etc/yum.repos.d/bak

#2 创建阿里云yum源
# 没有wget 则先下载再上传
wget -O /etc/yum.repos.d/aliyun.repo http://mirrors.aliyun.com/repo/Centos-7.repo

#3 清理并重新加载yum源
yum clean all && yum makecache

yum update -y

yum install net-tools \
yum install vim	\
yum install wget \
yum install unzip
```

## 桥接模式

### 还原默认设置

![image-20240904201408427](https://img.myfox.fun/img/image-20240904201408427.png)

![image-20240904201447083](https://img.myfox.fun/img/image-20240904201447083.png)

### 配置1

```sh
1.  cd    /etc/sysconfig/network-scripts/ifcfg-"网卡的名字"
2.  vi    ifcfg-"网卡的名字"    
```

注意：下面网关和子网掩面和主机保持一致，ip要和主机是一个网段下，找一个可以ping通的DNS

```sh
TYPE="Ethernet"
PROXY_METHOD="none"
BROWSER_ONLY="no"
BOOTPROTO="static"			// 静态	
IPADDR="192.168.101.120"  //这个是访问我们虚拟机的IP，IP的前三段跟主机一样，最后一段我们自定义，不冲突即可
GATEWAY="192.168.101.1"   #这个网关ip和自己主机的网关ip保持一致
NETMASK="255.255.255.0"   #子网掩码跟自己主机的也保持一致
DNS1="8.8.8.8"            //通过将你的默认DNS改为谷歌的公共DNS服务器
DNS2="8.8.4.4"            //Google公共DNS服务器备用地址
DEFROUTE="yes"				
IPV4_FAILURE_FATAL="no"
IPV6INIT="yes"
IPV6_AUTOCONF="yes"
IPV6_DEFROUTE="yes"
IPV6_FAILURE_FATAL="no"
IPV6_ADDR_GEN_MODE="stable-privacy"
NAME="ens33"
UUID="d8fbbece-3798-40d7-9333-351a58f*****"
DEVICE="ens33"
ONBOOT="yes" # 启用网卡
```

