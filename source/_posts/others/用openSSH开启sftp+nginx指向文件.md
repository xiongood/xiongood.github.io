---
title: 用openSSH开启sftp+nginx访问文件
author: 张一雄
summary: 这样可以做文件储存服务器，感觉非常的方便！以后不用fastDfs了！
img: https://pub-b24cf0a8c1f14e9386435977aa464959.r2.dev/img/sftp.jpeg
categories:
 - 周边
tags:
 - sftp
 - openSSH
 - linux
 - nginx
---

## 开启sftp

CentOS 自带openssh，不用在安装

```sh
yum install openssh-server
```

- 新建用户

```sh
useradd zhang
# 或者 adduser zhang
# 修改密码
passwd zhang

# 新增第二个
adduser osmond
passwd osmond

# 新增第三个
useradd yixiong
passwd yixiong
```

- 修改openssh的配置文件

```sh
vim /etc/ssh/sshd_config
```

```properties
# 第一行必须是注释
HostKey /etc/ssh/ssh_host_rsa_key
HostKey /etc/ssh/ssh_host_ecdsa_key
HostKey /etc/ssh/ssh_host_ed25519_key
SyslogFacility AUTHPRIV
AuthorizedKeysFile	.ssh/authorized_keys
PasswordAuthentication yes
ChallengeResponseAuthentication no
# 这个改为no，否则有可能会影响用户登录速度
GSSAPIAuthentication no
GSSAPICleanupCredentials no
UsePAM yes
X11Forwarding yes
AcceptEnv LANG LC_CTYPE LC_NUMERIC LC_TIME LC_COLLATE LC_MONETARY LC_MESSAGES
AcceptEnv LC_PAPER LC_NAME LC_ADDRESS LC_TELEPHONE LC_MEASUREMENT
AcceptEnv LC_IDENTIFICATION LC_ALL LANGUAGE
AcceptEnv XMODIFIERS
Subsystem	sftp	/usr/libexec/openssh/sftp-server

# 设置SSH的端口号是22(默认端口号为22)
Port 22  
# 启用SSH版本2协议
Protocol 2  
# 设置服务监听的地址 
# 监听所有地址： 0.0.0.0 
# 监听多个地址： 192.168.1.1，192.168.1.2
# 监听范围：192.168.0.0/24 （从192.168.0.0到192.168.0.255）
ListenAddress 0.0.0.0
# 拒绝访问的用户(用空格隔开)
DenyUsers  zhang  
#允许访问的用户(用空格隔开) （自己的服务必须得有root，要不然root无法用xshell登录了）里面的root必须要有，root否则无法登录
AllowUsers  root osmond vivek  
# 禁止root用户登陆（yes 为不禁止）
PermitRootLogin  yes
# 用户登陆需要密码认证
PermitEmptyPasswords no  
# 启用口令认证方式
PasswordAuthentication  yes  
# 不设置这个 用户登录会特别慢
UseDNS no
```

- 启动

```sh
# 启动
sudo systemctl start sshd
# 重启
sudo systemctl restart sshd
netstat -nltp
# 查看状态
systemctl status sshd.service
```

- 关闭防火墙

```sh
#这个亲测可用
systemctl stop firewalld.service
#开机禁止启动
systemctl disable firewalld.service
```

- 连接

```sh
# 这个可以进入
sftp osmond@localhost

# 这个不能进入 配置文件中写了不能登录
sftp zhang@localhost

# 这个也不能登录 配置文件写了root不能登录
sftp root@localhost
1
# 这个也不能登录 因为配置文件里没有写
sftp yixiong@localhost
```

- 权限(给sftp用户权限)

```sh
# 子目录的文件赋予osmond操作权限
su root
chown -R  osmond:osmond /home/osmond/
# 切换目录
su osmond
# 赋予权限 
chmod 777 /home/osmond/
```

## 安装nginx

- 安装依赖

```sh
yum install gcc-c++
yum install -y openssl openssl-devel
yum install -y pcre pcre-devel
yum install -y zlib zlib-devel
yum install wget
```

- 下载安装启动

```sh
wget https://nginx.org/download/nginx-1.19.9.tar.gz
tar -zxvf nginx-1.19.9.tar.gz
cd nginx-1.19.9
./configure
make
make install
whereis nginx
cd sbin
./nginx
ps -ef | grep nginx
```

- 常用命令

```sh
cd /usr/local/nginx/sbin/
# 重新加载配置
./nginx -s reload
#启动
nginx 
# 停止
./nginx -s quit 	#:此方式停止步骤是待nginx进程处理任务完毕进行停止。
./nginx -s stop 	#:此方式相当于先查出nginx进程id再使用kill命令强制杀掉进程。
```

- 修改配置文件

```sh
worker_processes  1;

events {
    worker_connections  1024;
}

http {
    include       mime.types;
    default_type  application/octet-stream;
    sendfile        on;
    keepalive_timeout  65;

    server {
        listen       9999;
        server_name  localhost;

        location / {
             autoindex on;
             root  /opt/image;
        }
        error_page   500 502 503 504  /50x.html;
        location = /50x.html {
            root   html;
        }
    }
}
```

- 修改配置文件（方式二：只匹配图片）

```c#
worker_processes  1;

events {
    worker_connections  1024;
}

http {
    include       mime.types;
    default_type  application/octet-stream;
    sendfile        on;
    keepalive_timeout  65;

    server {
        listen       9999;
        server_name  localhost;

        location ~*.(gif|jpg|jpeg)$ {
                autoindex on;
                root  /opt;
        }
        error_page   500 502 503 504  /50x.html;
        location = /50x.html {
            root   html;
        }
    }
}
```



- 重启后访问

```sh
http://192.168.31.221:9999/
```

## java连接sftp

```http
https://gitee.com/erhu02/demo
```



