---
title: cetos7安装gitlib
summary: 私域的git，每个公司的必备工具。当然也可以用github、gitee等！
img: https://pub-b24cf0a8c1f14e9386435977aa464959.r2.dev/img/gitlib.jpg
categories:
 - 工具
tags:
 - gitlib
 - centos7
---

## 安装依赖

### 安装ssh

```shell
sudo yum install -y curl policycoreutils-pythonopenssh-server
```

### 启动sshd

```shell
sudo systemctl start sshd
```

### 安装发送邮件工具

```shell
# 安装
sudo yum install postfix
# 开机启动
sudo systemctl enable postfix
# 启动
sudo systemctl start postfix
```

## 安装gitlib

### 下载地址

清华源

```http
https://mirrors.tuna.tsinghua.edu.cn/gitlab-ce/yum/el7/
```

### 下载命令

```shell
wget https://mirrors.tuna.tsinghua.edu.cn/gitlab-ce/yum/el7/gitlab-ce-10.0.0-ce.0.el7.x86_64.rpm
# 证书到期后用下面的命令
wget https://mirrors.tuna.tsinghua.edu.cn/gitlab-ce/yum/el7/gitlab-ce-10.0.0-ce.0.el7.x86_64.rpm --no-check-certificate
# 换目录
mv gitlab-ce-10.0.0-ce.0.el7.x86_64.rpm /opt/gitlab/
```

### 安装

```sh
# 安装依赖
policycoreutils-python
# 安装
rpm -i gitlab-ce-10.0.0-ce.0.el7.x86_64.rpm
```

### 修改端口号

```shell
vim  /etc/gitlab/gitlab.rb

external_url 'http://localhost:8888'
```

### 重置并启动

```shell
# 重置（时间比较长）
gitlab-ctl reconfigure
# 启动
gitlab-ctl restart
```

### 访问

```http
http://192.168.43.111:8888/
```

初次访问需要修改密码

默认账号：root

密码：自己设置的

## 其他设置

### 设置分支

新建的项目，新建的项目，其他人无法直接使用master分支，所以需要新增几个分支进行开发

### 修改自己的邮箱

![image-20230615102956275](https://pub-b24cf0a8c1f14e9386435977aa464959.r2.dev/img/20230615102957.png)



