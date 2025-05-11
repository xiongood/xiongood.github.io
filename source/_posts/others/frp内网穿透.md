---
title: frp内网穿透
author: 张一雄
summary: 好多的内网穿透工具都收费的，有的被挡在了网络长城外面，这个也得又一个云服务器才能使用！
img: https://img.myfox.fun/img/frp.jpg
categories:
 - 周边
tags:
 - frp
 - linux
---

### 准备：

#### 一个具有公网ip的主机

#### 官网：

```http
https://open.dingtalk.com/document/resourcedownload/alibaba-cloud-frp-intranet-penetration-tool
```

```http
https://gofrp.org/docs/setup/
```

### 搭建服务端

- 安装

```sh
wget https://github.com/fatedier/frp/releases/download/v0.48.0/frp_0.48.0_linux_amd64.tar.gz
tar -xvf frp_0.38.0_linux_amd64.tar.gz 
mkdir /usr/local/frp
mv frp_0.38.0_linux_amd64/* /usr/local/frp/
```

- 配置

```sh
cd /usr/local/frp
vi frps.ini
```

```properties
[common]
bind_port = 7000
vhost_http_port = 80 #监听http的端口

[web-http] 
listen_port=80 # 监听http的端口

# 尽量不要再配置文件中写注释……
```

- 启动(非控制台)

```sh
./frps -c ./frps.ini
```

- 静寂启动

```SH
# yum
yum install systemd
# apt
apt install systemd
# 新增脚本 frp_0.48.0_linux_amd64
vim /etc/systemd/system/frps.service
```

```properties
[Unit]
# 服务名称，可自定义
Description = frp server
After = network.target syslog.target
Wants = network.target

[Service]
Type = simple
# 启动frps的命令，需修改为您的frps的安装路径
ExecStart = /usr/local/frp/frps -c /usr/local/frp/frps.ini

[Install]
WantedBy = multi-user.target
```

- 启动命令

```sh
# 启动frp
systemctl start frps
# 停止frp
systemctl stop frps
# 重启frp
systemctl restart frps
# 查看frp状态
systemctl status frps
```

- 设置开机启动

```sh
systemctl enable frps
```

### 搭建客户端

#### windows http

- 下载

  ```http
  https://github.com/fatedier/frp/releases/tag/v0.48.0
  ```

- 修改配置文件

  ```properties
  [common]
  server_addr = myfox.fun
  server_port = 7000
  
  
  [web-http]
  type = http
  local_port = 9081 
  remote_port = 80 
  local_ip = 127.0.0.1
  custom_domains = myfox.fun
  
  #尽量不要在配置文件中写注释
  ```

- 访问

  ```http
  http://myfox.fun/api-interfaces/services
  ```

#### linux ssh

- 下载

  frp_0.48.0_linux_amd64.tar.gz

- 修改配置文件

  ```properties
  [common]
  server_addr = myfox.fun
  server_port = 7000
  
  [ssh]
  type = tcp
  local_ip = 127.0.0.1
  local_port = 22
  remote_port = 6000
  ```

- 启动

  ```sh
  ./frpc -c ./frpc.ini
  ```
