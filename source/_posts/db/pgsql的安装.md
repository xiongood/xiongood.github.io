---
title: pgsql的安装
img: https://pub-b24cf0a8c1f14e9386435977aa464959.r2.dev/img/20230816091040.png
categories:
 - 数据库
tags:
 - pgsql
 - linux
---

环境：centos7

#### 检查安装源

```sh
yum search postgresql
```

#### 安装

```sh
yum install postgresql-server
```

#### 常用命令

```sh
which psql
# /usr/bin/psql
which postgresql-setup
# /usr/bin/postgresql-setup
whereis postgresql-setup
# postgresql-setup: /usr/bin/postgresql-setup /usr/share/man/man1/postgresql-setup.1.gz
```

#### 查看版本号

```sh
psql --version
```

### 初始化

安装完成之后，不能直接启动数据库，需要先执行初始化，初始化之后，会生成postgresql相关配置文件和数据库文件，他们都会存放在路径/var/lib/pgsql/data下。

#### 初始化

```sh
postgresql-setup initdb
```

#### 检查数据库存储路径

```sh
cd /var/lib/pgsql/data

ll
```

#### 结果

```
drwx------. 5 postgres postgres    41 7月  20 16:13 base
drwx------. 2 postgres postgres  4096 7月  20 16:13 global
drwx------. 2 postgres postgres    18 7月  20 16:13 pg_clog
-rw-------. 1 postgres postgres  4232 7月  20 16:13 pg_hba.conf
-rw-------. 1 postgres postgres  1636 7月  20 16:13 pg_ident.conf
drwx------. 2 postgres postgres     6 7月  20 16:13 pg_log
drwx------. 4 postgres postgres    36 7月  20 16:13 pg_multixact
drwx------. 2 postgres postgres    18 7月  20 16:13 pg_notify
drwx------. 2 postgres postgres     6 7月  20 16:13 pg_serial
drwx------. 2 postgres postgres     6 7月  20 16:13 pg_snapshots
drwx------. 2 postgres postgres     6 7月  20 16:13 pg_stat_tmp
drwx------. 2 postgres postgres    18 7月  20 16:13 pg_subtrans
drwx------. 2 postgres postgres     6 7月  20 16:13 pg_tblspc
drwx------. 2 postgres postgres     6 7月  20 16:13 pg_twophase
-rw-------. 1 postgres postgres     4 7月  20 16:13 PG_VERSION
drwx------. 3 postgres postgres    60 7月  20 16:13 pg_xlog
-rw-------. 1 postgres postgres 19844 7月  20 16:13 postgresql.conf
```

### 启动

```sh
service postgresql start
service postgresql stop
```

#### 查看是否启动成功

```sh
netstat -nat
# 或者
ps -ef | grep pgsql
```

存在 5432 端口表示启动成功

#### 登录

```sh
su postgres 

bash-4.2$ psql
psql (9.2.24)
输入 "help" 来获取帮助信息.

postgres=#
```

##### 常用命令

```
\h：查看SQL命令的解释，比如\h select。
\?：查看psql命令列表。
\l：列出所有数据库。
\c [database_name]：连接其他数据库。
\d：列出当前数据库的所有表格。
\d [table_name]：列出某一张表格的结构。
\du：列出所有用户。
\e：打开文本编辑器。
\conninfo：列出当前数据库和连接的信息。
```

#### 设置外网链接

```sh
cd /var/lib/pgsql/data

vim pg_hba.conf
# 在文件下面添加一行：
# host  all  all  0.0.0.0/0  md5

vim postgresql.conf 
#修改
#listen_addresses = '*' 

重启
service postgresql start
service postgresql stop
```

#### 修改默认密码

```sh
sudo -u postgres psql

# postgres=# 

ALTER USER postgres WITH PASSWORD 'postgres';

# 返回客户端

# postgres-# \q

重启
service postgresql start
service postgresql stop
```

至此安装完成

