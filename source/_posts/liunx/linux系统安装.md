---
title: CentOS7系统安装
summary: centos7的安装以及网络的配置
img: https://pub-b24cf0a8c1f14e9386435977aa464959.r2.dev/img/20230816091455.png
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

![image-20230421095147566](https://pub-b24cf0a8c1f14e9386435977aa464959.r2.dev/img/20230421095148.png)

### 阿里下载源

```http
https://mirrors.aliyun.com/centos/
```

## 安装

略……

## 配置

### 没有IP

![image-20230419111252942](https://pub-b24cf0a8c1f14e9386435977aa464959.r2.dev/img/image-20230419111252942.png)

- 修改配置文件

```sh
vi /etc/sysconfig/network-scripts/ifcfg-ens33
```



![image-20230419111308767](https://pub-b24cf0a8c1f14e9386435977aa464959.r2.dev/img/image-20230419111308767.png)

- 重启网络

```sh
systemctl restart network
ip addr
```

![image-20230419111318355](https://pub-b24cf0a8c1f14e9386435977aa464959.r2.dev/img/image-20230419111318355.png)

- 关闭虚拟机，设置网络连接模式

![image-20230419111326030](https://pub-b24cf0a8c1f14e9386435977aa464959.r2.dev/img/image-20230419111326030.png)

### ping 不通百度

![image-20240828170513587](https://pub-b24cf0a8c1f14e9386435977aa464959.r2.dev/img/image-20240828170513587.png)

编辑》虚拟机网络配置器

![image-20240828170539134](https://pub-b24cf0a8c1f14e9386435977aa464959.r2.dev/img/image-20240828170539134.png)

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
yum install net-tools
yum install vim
yum install wget
# yum install tar
```

![image-20230419111336458](https://pub-b24cf0a8c1f14e9386435977aa464959.r2.dev/img/image-20230419111336458.png)

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
```
