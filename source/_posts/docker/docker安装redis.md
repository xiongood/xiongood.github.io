---
title: docker安装redis
img: https://img.myfox.fun/img/redis.jpg
categories:
 - 周边
tags:
 - redis
 - coenos7
 - docker
---

## 安装

### 拉取镜像

```sh
docker pull redis:6.2.6
docker images
```

### 创建reids配置文件

```sh
# 1-新建文件夹
mkdir -p /data/dockerData/redis/conf
cd /data/dockerData/redis/conf
 
# 2-创建文件
touch redis.config
ls
vim redis.config 
```

写入：

```sh
# Redis服务器配置 
 
# 绑定IP地址
#解除本地限制 注释bind 127.0.0.1  
#bind 127.0.0.1  
 
# 服务器端口号  
port 6379 
 
#配置密码，不要可以删掉
requirepass 123456
  
 
 
#这个配置不要会和docker -d 命令 冲突
# 服务器运行模式，Redis以守护进程方式运行,默认为no，改为yes意为以守护进程方式启动，可后台运行，除非kill进程，改为yes会使配置文件方式启动redis失败，如果后面redis启动失败，就将这个注释掉
daemonize no
 
#当Redis以守护进程方式运行时，Redis默认会把pid写入/var/run/redis.pid文件，可以通过pidfile指定(自定义)
#pidfile /data/dockerData/redis/run/redis6379.pid  
 
#默认为no，redis持久化，可以改为yes
appendonly yes
 
 
#当客户端闲置多长时间后关闭连接，如果指定为0，表示关闭该功能
timeout 60
# 服务器系统默认配置参数影响 Redis 的应用
maxclients 10000
tcp-keepalive 300
 
#指定在多长时间内，有多少次更新操作，就将数据同步到数据文件，可以多个条件配合（分别表示900秒（15分钟）内有1个更改，300秒（5分钟）内有10个更改以及60秒内有10000个更改）
save 900 1
save 300 10
save 60 10000
 
# 按需求调整 Redis 线程数
tcp-backlog 511
 
 
 
  
 
 
# 设置数据库数量，这里设置为16个数据库  
databases 16
 
 
 
# 启用 AOF, AOF常规配置
appendonly yes
appendfsync everysec
no-appendfsync-on-rewrite no
auto-aof-rewrite-percentage 100
auto-aof-rewrite-min-size 64mb
 
 
# 慢查询阈值
slowlog-log-slower-than 10000
slowlog-max-len 128
 
 
# 是否记录系统日志，默认为yes  
syslog-enabled yes  
 
#指定日志记录级别，Redis总共支持四个级别：debug、verbose、notice、warning，默认为verbose
loglevel notice
  
# 日志输出文件，默认为stdout，也可以指定文件路径  
logfile stdout
 
# 日志文件
#logfile /var/log/redis/redis-server.log
 
 
# 系统内存调优参数   
# 按需求设置
hash-max-ziplist-entries 512
hash-max-ziplist-value 64
list-max-ziplist-entries 512
list-max-ziplist-value 64
set-max-intset-entries 512
zset-max-ziplist-entries 128
zset-max-ziplist-value 64
```

### 启动

```sh
docker run -p 6379:6379 --name redis6.2.6 -v /data/dockerData/redis/conf/redis.config:/etc/redis/redis.conf -v /data/dockerData/redis/data:/var/lib/redis -v /data/dockerData/redis/logs:/logs -d redis:6.2.6 redis-server /etc/redis/redis.conf

docker ps -a
```

说明：

```sh
–privileged=true ：容器内的root拥有真正root权限，否则容器内root只是外部普通用户权限

-p：端口映射，此处映射 主机6379端口 到 容器的6379端口

-v：主机和容器的目录映射关系，":"前为主机目录，之后为容器目录

新建配置文件书卷：  -v /data/dockerData/redis/conf/redis.config:/etc/redis/redis.config

redis数据保存数据卷  -v /data/dockerData/redis/data:/var/lib/redis

reids日志文数据卷  -v /data/dockerData/redis/logs:/logs

-d : 表示使得容器后台一直运行
redis-server /etc/redis/redis.conf：指定配置文件启动redis-server进程
–appendonly yes：开启数据持久化
–requirepass 123456 ：设置你的密码，设置密码比较安全
```

