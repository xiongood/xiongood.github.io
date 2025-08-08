---
title: wsl的安装与使用
summary: 更加丝滑的虚拟机
categories:
 - wsl
tags:
 - wsl
---



## 使用

### 安装

```http
https://github.com/microsoft/WSL/releases/tag/2.5.10
```

### 安装使用Ubuntu

- 安装

```sh
# 查看可以安装的系统镜像
wsl --list --verbose
# 安装选择的系统镜像
wsl.exe --install Ubuntu-22.04
```

- 修改root密码

```sh
sudo passwd root
```

- 安装ip工具

```sh
apt install net-tools
ifconfig
```

- 关机

```sh
# 退出窗口后执行
wsl --shutdown
```

- 开机

```sh
wsl
```

- 关闭防火墙

```sh
sudo ufw status
sudo ufw disable
sudo systemctl stop ufw
sudo systemctl mask ufw
```

## 技巧

### 进入主机的桌面 可以直接复制文件

```sh
# 宿主接桌面路径
/mnt/c/Users/xiong/Desktop
# 创建软连接
ln -s /mnt/c/Users/xiong/Desktop ./desktop
# 删除软连接
rm desktop
```

