---
title: linux常用命令日常总结
summary: 在学习和工作中，遇到了不熟悉的命令，我就将其写在此博客下，持续更新
img: https://pub-b24cf0a8c1f14e9386435977aa464959.r2.dev/img/20230816091455.png
categories:
 - linux
tags:
 - linux
---

## 时间

### 设置时区

```shell
timedatectl #查看当前时间与时区
timedatectl set-timezone Asia/Shanghai  #设置时区，如果时区不对需要设置
timedatectl set-time "YYYY-MM-DD HH:MM:SS"   #手动设置时间
```

### 自动校准时间

网络时间协议（NTP）是一种使计算机时间同步化的协议。它可以使计算机与互联网上的精确时间服务器同步，从而自动调整系统时间。

首先，确认你的系统已经安装了 chrony 包，如果没有，请执行以下命令安装：

```shell
sudo yum install chrony
```

然后，启动 chronyd 服务：

```shell
sudo systemctl start chronyd
```

并且设置开机自启：

```shell
sudo systemctl enable chronyd
```

最后，你可以使用以下命令确认时间同步状态：

```shell
chronyc tracking
```


这样，你的系统时间就会自动与网络上的标准时间保持同步。

## 查看文本

### 查看不是已“#”开头的行且不展示空白行

```sh
awk 'NF' postgresql.conf | grep -v '#'
```

