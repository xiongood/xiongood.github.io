---
title: 使用Cloudreve搭建私人网盘
author: 张一雄
summary: 随着阿里网盘的限速，我找到了这个私人网盘工具，不过网盘的尽头应该是NAS吧。
img: https://pub-b24cf0a8c1f14e9386435977aa464959.r2.dev/img/cloudreve.jpg
categories:
 - 周边
tags:
 - linux
 - Cloudreve
---

## linux

### 环境： 

centos7

## 官网

```http
https://docs.cloudreve.org/
```

### 安装

- 创建文件夹

```sh
mkdir /usr/local/cloudreve
cd /usr/local/cloudreve
```

- 下载

```http
https://github.com/cloudreve/Cloudreve/releases
```

- 解压

```sh
tar -zxvf cloudreve_3.7.1_linux_amd64.tar.gz
```

- 运行(看管理员账号密码)

```sh
# 赋予执行权限
chmod +x ./cloudreve

# 启动 Cloudreve（看管理员账号密码）
./cloudreve
```

- 重置管理员密码

```sh
./cloudreve --database-script ResetAdminPassword

# 默认账号
admin@cloudreve.org
# 密码
随机字符
```

- 访问

```http
localhost:5212
```

- ==注==

  必须登录一下管理员，修改下载链接，否则无法下载

### 守护进程

- 编辑配置文件

```sh
# 编辑配置文件
vim /usr/lib/systemd/system/cloudreve.service
```

```properties
[Unit]
Description=Cloudreve
Documentation=https://docs.cloudreve.org
After=network.target
After=mysqld.service
Wants=network.target

[Service]
WorkingDirectory=/PATH_TO_CLOUDREVE
ExecStart=/PATH_TO_CLOUDREVE/cloudreve
Restart=on-abnormal
RestartSec=5s
KillMode=mixed

StandardOutput=null
StandardError=syslog

[Install]
WantedBy=multi-user.target
```

- 常用命令

```sh
# 更新配置
systemctl daemon-reload

# 启动服务
systemctl start cloudreve

# 设置开机启动
systemctl enable cloudreve

# 启动服务
systemctl start cloudreve

# 停止服务
systemctl stop cloudreve

# 重启服务
systemctl restart cloudreve

# 查看状态
systemctl status cloudreve
```

## 使用

### 更改默认空间

点击我的头像->管理面板->用户组

## windiws(略)
