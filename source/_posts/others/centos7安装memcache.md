---
title: centos7安装memcached
author: 张一雄
summary: 缓存工具
img: https://img.myfox.fun/img/memcached.jpg
categories:
 - 工具
tags:
 - memcached
---

安装

```sh
# 下载
sudo yum install memcached libmemcached -y
# 配置
vim /etc/sysconfig/memcached
```

默认的例子

```sh
PORT="11211"
USER="memcached"
MAXCONN="1024"
CACHESIZE="64"
OPTIONS=""
```

常用命令

```sh
# 启动
sudo systemctl start memcached
# 开机自己启动
sudo systemctl enable memcached
# 查看状态
sudo systemctl status memcached
# 停止
sudo systemctl stop memcached

```

