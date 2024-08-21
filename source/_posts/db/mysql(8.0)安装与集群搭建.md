---
title: mysql(8.0)的安装及集群搭建
img: https://pub-b24cf0a8c1f14e9386435977aa464959.r2.dev/img/20230816090932.png
categories:
 - 数据库
tags:
 - mysql
---

## 环境

CentOS7  三台

mysql-8.0.33

## 下载与安装

### 官网

```http
https://www.mysql.com/
```

### 下载

- 划到最下面

![image-20230420214245838](https://pub-b24cf0a8c1f14e9386435977aa464959.r2.dev/img/20230420214247.png)

![image-20230420220711413](https://pub-b24cf0a8c1f14e9386435977aa464959.r2.dev/img/20230420220712.png)

![image-20230420214807804](https://pub-b24cf0a8c1f14e9386435977aa464959.r2.dev/img/20230420214809.png)

- 下载地址：


```http
https://cdn.mysql.com//Downloads/MySQL-8.0/mysql-8.0.33-linux-glibc2.12-x86_64.tar.xz
```

### 安装

```shell
# 安装依赖
# search for info
yum search libaio  
# install library
yum install libaio 
yum install ncurses-compat-libs

# 创建用户组
groupadd mysql
useradd -r -g mysql -s /bin/false mysql

# 安装mysql
# 下载
cd 
wget https://cdn.mysql.com//Downloads/MySQL-8.0/mysql-8.0.33-linux-glibc2.12-x86_64.tar.xz
# 解压
tar xvf mysql-8.0.33-linux-glibc2.12-x86_64.tar.xz
mv mysql-8.0.33-linux-glibc2.12-x86_64 /usr/local/mysql

cd /usr/local/mysql

mkdir mysql-files
chown mysql:mysql mysql-files
chmod 750 mysql-files

# 初始化，会报出来 一个root密码，注意保存
# A temporary password is generated for root@localhost: #LK)=okMo2Go
./bin/mysqld --initialize --user=mysql
# 删除初始化的内容
# rm -rf /var/lib/mysql/*

bin/mysql_ssl_rsa_setup
bin/mysqld_safe --user=mysql &
# 可选命令（方便启动）
cp support-files/mysql.server /etc/init.d/mysql.server
cp -a ./support-files/mysql.server /etc/init.d/mysql

# 添加环境变量
export PATH=$PATH:/usr/local/mysql/mysql/bin

# 创建日志文件(没有则创建)
mkdir -p /var/log/mariadb/
vim /var/log/mariadb/mariadb.log
chown mysql /var/log/mariadb/mariadb.log
chmod 777 /var/log/mariadb/mariadb.log
```

## 启动与配置

### 启动

```sh
# 方式一
service mysql start
service mysql stop
service mysql restart

# 方式二（也可以不进此文件夹）
cd /usr/local/mysql/support-files
# 启动
./mysql.server start
# 停止
./mysql.server stop

# 查看端口号
netstat -nltp
# 查看pid
ps -ef | grep mysql
```

### 设置开机启动

```sh
# 设置开机启动
chmod +x /etc/init.d/mysql
chkconfig --add mysql
# 查看开机启动列表，345为“开”则成功
chkconfig --list
# 重启测试
```

### 修改root密码

- 修改配置文件

```sh
# 如果没有[client]标签则新增，如果有则不用管了
vim /etc/my.cnf
```

```sh
# 新增
[client]
port=3306
# 和server中的值一样
socket=/var/lib/mysql/mysql.sock
# 启动
service mysql restart
```

完整的配置文件

```sh
cat /etc/my.cnf | grep -v "#"
```

```sh
[mysqld]
datadir=/var/lib/mysql
socket=/var/lib/mysql/mysql.sock
symbolic-links=0

[mysqld_safe]
log-error=/var/log/mariadb/mariadb.log
pid-file=/var/run/mariadb/mariadb.pid

[client]
port=3306
socket=/var/lib/mysql/mysql.sock

!includedir /etc/my.cnf.d
```

- 登录

```sh
# 登录
cd /usr/local/mysql/bin
./mysql -u root -p
alter user user() identified by "123456";
# 修改root可远程访问
use mysql;
# 查询
select host,user from user;
# 修改
update user set host='%' where user='root';
flush privileges;
# 查询
select host,user from user;
```

##  集群的搭建

### 说明

创建三台服务器，都安装mysql

其中1台为master，两台问slave

### 准备

如果是复制的 虚拟机，则需要将这个文件删除后重启，此文件会再次自动生成

里面的uuid，如果多个服务器间有重复的话，无法进行主从复制

```sh
# 查询这个文件
find / -iname "auto.cnf"
# 删除这个文件（会自己生成）
rm -rf  /var/lib/mysql/auto.cnf 
# 重启
service mysql restart
```

### 配置master

#### 修改配置文件

```sh
vim /etc/my.cnf
```

```sh
# 在[mysqld]下新增
# id
server-id=1
# 日志格式
binlog_format=STATEMENT
```

完整的

```sh
[mysqld]
server-id=1
binlog_format=STATEMENT
datadir=/var/lib/mysql
socket=/var/lib/mysql/mysql.sock
symbolic-links=0

[mysqld_safe]
log-error=/var/log/mariadb/mariadb.log
pid-file=/var/run/mariadb/mariadb.pid

[client]
port=3306
socket=/var/lib/mysql/mysql.sock

!includedir /etc/my.cnf.d
```

```sh
# 重启
service mysql restart
```

#### 创建账号

从服务器访问主服务器用

```sql
use mysql
-- 创建用户
create user 'slave'@'%';
-- 设置密码
ALTER USER 'slave'@'%' IDENTIFIED WITH mysql_native_password by '123456'

-- 授予复制权限
GRANT replication slave on *.* to 'slave'@'%';

-- 刷新权限
FLUSH PRIVILEGES
```

#### 查看主机状态

从数据库，会从我们指定的日志文件和位置 来读取日志进行备份

```sql
show MASTER STATUS;
-- binlog.000009 为日志文件名称
-- 1063 为当前日志位置
```

![image-20230420235342622](https://pub-b24cf0a8c1f14e9386435977aa464959.r2.dev/img/20230420235343.png)

### 配置slave

#### 修改配置文件

```sh
vim /etc/my.cnf
```

```sh
[mysqld]
# 新增id，都不能重复
server-id=3
datadir=/var/lib/mysql
socket=/var/lib/mysql/mysql.sock
symbolic-links=0

[mysqld_safe]
log-error=/var/log/mariadb/mariadb.log
pid-file=/var/run/mariadb/mariadb.pid

[client]
port=3306
socket=/var/lib/mysql/mysql.sock

!includedir /etc/my.cnf.d
```

```sh
# 重启
service mysql restart
```

#### 在从库配置主数据库信息

```sql
-- 不用切换 mysql 库
-- 8.0.22版本前
CHANGE MASTER TO MASTER_host = '192.168.31.17', -- 主机ip
MASTER_user = 'slave', -- 登录名
master_password = '123456', -- 登录密码
MASTER_port = 3306, -- 主机端口
MASTER_log_file = 'binlog.000009',-- 主机日志名
MASTER_log_pos = 1063; -- 主机日志位置

-- 8.0.22版本后
CHANGE REPLICATION SOURCE TO SOURCE_HOST = '192.168.31.17',
SOURCE_PORT = 3306,
SOURCE_USER = 'slave',
SOURCE_PASSWORD = '123456',
SOURCE_LOG_FILE = 'binlog.000009',
SOURCE_LOG_POS = 1453;
```

## 测试主从复制

### 在从数据库中启动主从复制

```sql
-- 8.0.22版本前
START slave;
stop  slave;
SHOW slave STATUS;

-- 8.0.22版本后
START REPLICA;
stop  REPLICA;
SHOW REPLICA STATUS;
```

其中,这两个都是yes，则成功

```sh
Slave_IO_Running: Yes
Slave_SQL_Running: Yes
```

### 问题：Slave_IO_Running: No

```sh
# 查询这个文件
find / -iname "auto.cnf"
# 删除这个文件（会自己生成）
rm -rf  /var/lib/mysql/auto.cnf 
# 重启mysql
service mysql restart
# 重启复制
stop  slave;
START slave;
# 查看状态
SHOW slave STATUS;
```

### 问题：Slave_SQL_Running: No

#### 方式一（直接用第二个）

```sql
-- 查看主库状态
show MASTER STATUS;

# 挺掉主从复制
STOP slave;
# 修改主机信息
CHANGE MASTER TO master_host = '192.168.31.17',
master_user = 'slave',
master_password = '123456',
master_log_file = 'binlog.000009',
master_log_pos = 1843;
# 启动复制
START slave;
# 查看状态
SHOW slave STATUS;
```

#### 方式二

```sql
-- 查看状态
SHOW slave STATUS;
-- 停止复制
stop  slave;
-- 跳过第一个错误
set GLOBAL SQL_SLAVE_SKIP_COUNTER=1;
-- 刷新从机状态
reset slave
# 修改主机信息
CHANGE MASTER TO master_host = '192.168.31.17',
master_user = 'slave',
master_password = '123456',
master_log_file = 'binlog.000009',
master_log_pos = 1843;
-- 启动从机
START slave;
-- 查看状态
SHOW slave STATUS;
```

### 测试

此时，在主库中新建表空间、表结构、新增表数据，在从库中都能看到了

```sql
CREATE DATABASE db_user;
USE db_user;
CREATE TABLE t_user (
 id BIGINT AUTO_INCREMENT,
 uname VARCHAR(30),
 PRIMARY KEY (id)
);
INSERT INTO t_user(uname) VALUES('zhang3');
INSERT INTO t_user(uname) VALUES(@@hostname);
```

## 特殊情况

### 问题一

问：让从机，做为主机，再为其创建从机是否可以

答：可以，每台数据库都同时作为主机和从机

### 问题二

问：从机停机一会儿，主机执行写操作，从机再启动，从机数据会恢复和主机一致吗？

答：从机启动后，会恢复数据与主机一致

### 问题三

问：第一台从机停机一会儿，主机做了写操作，之后停机（保留第二台主机），之后第一台从重启，之后主机重启，数据会恢复吗？

答：会回复

### 问题四

问：主机启动写了好多写操作后，启动新的从机，从机的数据会和主机保持一致吗

答：从机不会复制在建立主从关系之前的数据

