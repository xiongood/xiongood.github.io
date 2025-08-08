---
title: ubuntu开通ftp
summary: ubuntu开通ftp
categories:
 - ftp
tags:
 - ftp
---



### 更新

```sh
# 更新软件源
sudo apt update
```

### 安装

```sh
# 安装 FTP 服务器
sudo apt install vsftpd  

# 启动
# 启动服务
sudo systemctl start vsftpd  
# 设置开机自启
sudo systemctl enable vsftpd  

# 验证
sudo systemctl status vsftpd

# 修改配置
vim /etc/vsftpd.conf
```

#### 需要修改的配置

```sh
# 允许本地用户登录（默认可能已开启）
local_enable=YES

# 允许本地用户上传文件
write_enable=YES

# 限制用户只能访问自己的家目录（安全推荐）
chroot_local_user=YES
allow_writeable_chroot=YES  # 允许受限目录有写权限

# （可选）指定 FTP 端口（默认 21，可保持默认）
listen_port=21

# （可选）允许被动模式（如果客户端连接有问题，添加以下配置）
pasv_enable=YES
pasv_min_port=40000
pasv_max_port=50000
```

#### 完整的配置

```sh
listen=NO
listen_ipv6=YES
anonymous_enable=NO
local_enable=YES
dirmessage_enable=YES
use_localtime=YES
xferlog_enable=YES
connect_from_port_20=YES
secure_chroot_dir=/var/run/vsftpd/empty
pam_service_name=vsftpd
rsa_cert_file=/etc/ssl/certs/ssl-cert-snakeoil.pem
rsa_private_key_file=/etc/ssl/private/ssl-cert-snakeoil.key
ssl_enable=NO
write_enable=YES
chroot_local_user=YES
allow_writeable_chroot=YES
listen_port=21
pasv_enable=YES
pasv_min_port=40000
pasv_max_port=5000
```

### 重启

```sh
# 重启
sudo systemctl restart vsftpd
```

### 注意

2、ip可以直接写localhost

1、只能不能通过root在客户端登录！