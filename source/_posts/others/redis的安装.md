---
title: redis的安装
author: 张一雄
summary: 程序员最常用的中间件之一，该叫他缓存呢还是数据库呢？
img: https://pub-b24cf0a8c1f14e9386435977aa464959.r2.dev/img/20230816091932.png
categories:
 - 周边
tags:
 - redis
 - linux
---

## 环境

CentOS7 

redis6.2.5

## 下载

- 使用华为镜像

```sh
mkdir -p /opt/redis
ce /opt/redis
wget https://repo.huaweicloud.com/redis/redis-6.2.5.tar.gz
```

- 安装

```sh
# 安装依赖包
yum -y install gcc gcc-c++

# 解压
tar -zxvf redis-6.2.5.tar.gz
cd redis-6.2.5/

#编译
make MALLOC=libc
# 安装
cd src && make install
```

## 配置

- 修改配置

```sh
cd ..
vim redis.conf

#注释 这一行重新启动redis即可
#bind 127.0.0.1

#设置安全密码
requirepass 123456

# 静寂启动	
daemonize yes
```

## 启动

- 启动

```sh
cd src/
./redis-server ../redis.conf

# 查看是否启动
ps -aux | grep redis
```

- 设置开机启动

```sh
cd /etc
mkdir redis
cd redis
cp /opt/redis/redis-6.2.5/redis.conf /etc/redis/6379.conf
cp /opt/redis/redis-6.2.5/utils/redis_init_script /etc/init.d/redisd
cd /etc/init.d
chkconfig redisd on

# 以后启动方式可以用这种
service redisd start
service redisd stop
```

# 配置持久化

## 出处

```http
https://www.cnblogs.com/kismetv/p/9137897.html
```

## RDB

### 手动

```sh
#进入客户端
./redis-cli 

#执行命令
127.0.0.1:6379> save
```

### 自动

#### 修改redis.conf配置文件中的

```sh
#   save ""
save 900 1
save 300 10
save 60 10000
```

#### 说明

其中save 900 1的含义是：当时间到900秒时，如果redis数据发生了至少1次变化，则执行bgsave；save 300 10和save 60 10000同理。当三个save条件满足任意一个时，都会引起bgsave的调用。

在主从复制场景下，如果从节点执行全量复制操作，则主节点会执行bgsave命令，并将rdb文件发送给从节点

执行shutdown命令时，自动执行rdb持久化

### 存储路径

#### 修改redis.conf

名称

```properties
# The filename where to dump the DB

#此处为存储位置，dir配置指定目录，dbfilename指定文件名。默认是Redis根目录下的dump.rdb文件。
dbfilename dump.rdb 

# Remove RDB files used by replication in instances without persistence
```

路径

```properties
# Note that you must specify a directory here, not a file name.
dir ./
```

#### 启动加载

RDB文件的载入工作是在服务器启动时自动执行的，并没有专门的命令。但是由于AOF的优先级更高，因此当AOF开启时，Redis会优先载入AOF文件来恢复数据；只有当AOF关闭时，才会在Redis服务器启动时检测RDB文件，并自动载入。服务器载入RDB文件期间处于阻塞状态，直到载入完成为止。

## AOF

Redis服务器默认开启RDB，关闭AOF；要开启AOF，需要在配置文件中配置。

当AOF开启时，Redis启动时会优先载入AOF文件来恢复数据；只有当AOF关闭时，才会载入RDB文件恢复数据。

当AOF开启，但AOF文件不存在时，即使RDB文件存在也不会加载(更早的一些版本可能会加载，但3.0不会)

常用配置，redis.conf

```properties
- appendonly no：是否开启AOF
- appendfilename "appendonly.aof"：AOF文件名
- dir ./：RDB文件和AOF文件所在目录
- appendfsync everysec：fsync持久化策略
- no-appendfsync-on-rewrite no：AOF重写期间是否禁止fsync；如果开启该选项，可以减轻文件重写时CPU和硬盘的负载（尤其是硬盘），但是可能会丢失AOF重写期间的数据；需要在负载和安全性之间进行平衡
- auto-aof-rewrite-percentage 100：文件重写触发条件之一
- auto-aof-rewrite-min-size 64mb：文件重写触发提交之一
- aof-load-truncated yes：如果AOF文件结尾损坏，Redis启动时是否仍载入AOF文件
```

