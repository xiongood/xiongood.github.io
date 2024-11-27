---
title: centos7安装ftp
author: 张一雄
summary: 我们前端程序员所依赖的开发运行工具！
img: https://pub-b24cf0a8c1f14e9386435977aa464959.r2.dev/img/20230816090747.png
categories:
 - 工具
tags:
 - node-js
---

## 安装

### 安装

```sh
yum -y install vsftpd
```

### 修改配置

```sh
cd /etc/vsftpd/
cp vsftpd.conf vsftpd.conf_bak
vim vsftpd.conf
```

内容如下

```sh
# 是否开启匿名用户，匿名都不安全，默认NO
anonymous_enable=NO
# 允许本机账号登录FTP
# 这个设定值必须要为YES时，在/etc/passwd内的账号才能以实体用户的方式登入我们的vsftpd主机
local_enable=YES
# 允许账号都有写操作
write_enable=YES
# 本地用户创建文件或目录的掩码
# 意思是指：文件目录权限：777-022=755，文件权限：666-022=644
local_umask=022
# 进入某个目录的时候，是否在客户端提示一下
dirmessage_enable=YES
# 当设定为YES时，使用者上传与下载日志都会被记录起来
xferlog_enable=YES
# 日志成为std格式
xferlog_std_format=YES
# 上传与下载日志存放路径
xferlog_file=/var/log/xferlog
# 开放port模式的20端口的连接
connect_from_port_20=YES
# 关于系统安全的设定值：
# ascii_download_enable=YES(NO)
# 如果设定为YES，那么client就可以使用ASCII格式下载档案
# 一般来说，由于启动了这个设定项目可能会导致DoS的攻击，因此预设是NO
# ascii_upload_enable=YES(NO)
# 与上一个设定类似的，只是这个设定针对上传而言，预设是NO
ascii_upload_enable=NO
ascii_download_enable=NO
# 通过搭配能实现以下几种效果：
# ①当chroot_list_enable=YES，chroot_local_user=YES时，在/etc/vsftpd/chroot_list文件中列出的用户，可以切换到其他目录；未在文件中列出的用户，不能切换到其他目录
# ②当chroot_list_enable=YES，chroot_local_user=NO时，在/etc/vsftpd/chroot_list文件中列出的用户，不能切换到其他目录；未在文件中列出的用户，可以切换到其他目录
# ③当chroot_list_enable=NO，chroot_local_user=YES时，所有的用户均不能切换到其他目录
# ④当chroot_list_enable=NO，chroot_local_user=NO时，所有的用户均可以切换到其他目录
# 限制用户只能在自己的目录活动
chroot_local_user=YES
chroot_list_enable=NO
chroot_list_file=/etc/vsftpd/chroot_list
# 可以更改ftp的端口号，使用默认值21
# listen_port=60021
# 监听ipv4端口，开了这个就说明vsftpd可以独立运行，不用依赖其他服务
listen=NO
# 监听ipv6端口
listen_ipv6=YES
# 打开主动模式
port_enable=YES
# 启动被动式联机(passivemode)
pasv_enable=YES
# 被动模式端口范围：注意：linux客户端默认使用被动模式，windows 客户端默认使用主动模式。在ftp客户端中执行"passive"来切换数据通道的模式。也可以使用"ftp -A ip"直接使用主动模式。主动模式、被动模式是有客户端来指定的
# 上面两个是与passive mode使用的port number有关，如果您想要使用64000到65000这1000个port来进行被动式资料的连接，可以这样设定
# 这两项定义了可以同时执行下载链接的数量
# 被动模式起始端口，0为随机分配
pasv_min_port=64000
# 被动模式结束端口，0为随机分配
pasv_max_port=65000
# 文件末尾添加
# 这个是pam模块的名称，我们放置在/etc/pam.d/vsftpd，认证用
pam_service_name=vsftpd
# 使用允许登录的名单，在/etc/vsftpd/user_list文件中添加新建的用户snbftp
userlist_enable=YES
# 限制允许登录的名单，前提是userlist_enable=YES，其实这里有点怪,禁止访问名单在/etc/vsftpd/snbftp
userlist_deny=NO
# 允许限制在自己的目录活动的用户拥有写权限
# 不添加下面这个会报错：500 OOPS: vsftpd: refusing to run with writable root inside chroot()
allow_writeable_chroot=YES
# 当然我们都习惯支持TCP Wrappers的啦
# Tcp wrappers ： Transmission Control Protocol (TCP) Wrappers 为由 inetd 生成的服务提供了增强的安全性
tcp_wrappers=YES
# FTP访问目录
local_root=/data/ftp/snbftp
```

### 新建白名单

新建账户

```sh
sudo mkdir -p /data/ftp/
useradd -d /data/ftp/ -s /sbin/nologin snbftp
passwd snbftp
mkdir -pv /data/ftp
chown -R snbftp /data/ftp
# 密码123456
```

新增白名单，把用户加进去，一行一个

```sh
vim user_list
```

### 修改配置

```sh
vim /etc/pam.d/vsftpd
#注释下面一行
auth required pam_shells.so

vim /etc/vsftpd/vsftpd.conf
# 添加
allow_writeable_chroot=YES
```



### 启动

```sh
# 启动
systemctl start vsftpd
systemctl enable vsftpd.service && systemctl start vsftpd.service && systemctl status vsftpd.service
# 重启
systemctl restart vsftpd.service
```

