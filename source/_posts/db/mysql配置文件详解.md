---
title: mysql配置文件详解
img: https://pub-b24cf0a8c1f14e9386435977aa464959.r2.dev/img/mysql.jpg
categories:
 - 数据库
tags:
 - mysql
---

为了方便读者阅读，我们省略了 my.cnf 文件中的注释内容。下面分开介绍 my.cnf 中参数的具体意义，文件内容如下：

```
[client]
port=3306
socket=/var/run/mysql/mysql.sock
[mysqldump]
quick
max_allowed_packet = 16M
```

以上参数会被 MySQL 客户端应用读取，参数说明如下：

- port：MySQL 客户端连接服务器端时使用的端口号，默认为 3306
- socket：套接字文件所在目录
- quick：支持较大的数据库转储，导出非常巨大的表时需要此项 。
- max_allowed_packet：服务所能处理的请求包的最大大小以及服务所能处理的最大的请求大小（当与大的BLOB字段一起工作时相当必要），每个连接独立的大小，大小动态增加。

> 注意：只有 MySQL 附带的客户端应用程序保证可以读取这段内容。如果想要自己的 MySQL 应用程序获取这些值，需要在 MySQL 客户端库初始化的时候指定这些选项。

```
[mysqld]

user = mysql
basedir = /usr/local/mysql
datadir = /mydata/mysql/data
port=3306
server-id = 1
socket=/var/run/mysql/mysql.sock
```

上述参数说明如下：

- user：mysqld 程序在启动后将在给定 UNIX/Linux 账户下执行。mysqld 必须从 root 账户启动才能在启动后切换到另一个账户下执行。mysqld_safe 脚本将默认使用 user=mysql 选项来启动 mysqld 程序。
- basedir：指定 MySQL 安装的绝对路径；
- datadir：指定 MySQL 数据存放的绝对路径；
- port：服务端口号，默认为 3306
- server-id：MySQL 服务的唯一编号，每个 MySQL 服务的 id 需唯一。
- socket：socket 文件所在目录

```
character-set-server = utf8mb4
collation-server = utf8mb4_general_ci
init_connect='SET NAMES utf8mb4'
lower_case_table_names = 1

key_buffer_size=16M
max_allowed_packet=8M
no-auto-rehash
sql_mode=TRADITIONAL
```

- character-set-server：数据库默认字符集，主流字符集支持一些特殊表情符号（特殊表情符占用 4 个字节）
- collation-server：数据库字符集对应一些排序等规则，注意要和 character-set-server 对应
- init_connect：设置 client 连接 mysql 时的字符集，防止乱码
- lower_case_table_names：是否对 sql 语句大小写敏感，1 表示不敏感
- key_buffer_size：用于指定索引缓冲区的大小
- max_allowed_packet：设置一次消息传输的最大值
- no-auto-rehash：仅仅允许使用键值的 UPDATES 和 DELETES
- sql_mode：表示 SQL 模式的参数，通过这个参数可以设置检验 SQL 语句的严格程度
