---
title: mysql(5.7)的安装与卸载
img: https://pub-b24cf0a8c1f14e9386435977aa464959.r2.dev/img/mysql.jpg
categories:
 - 数据库
tags:
 - mysql
 - linux
---

环境：centos7

## Mysql安装

- 卸载Centos7自带的mariadb
  
  ```shell
  rpm -qa|grep mariadb
  mariadb-libs-5.5.64-1.el7.x86_64
  rpm -e mariadb-libs-5.5.64-1.el7.x86_64 --nodeps
  rpm -qa|grep mariadb
  ```

- 安装mysql
  
  ```shell
  mkdir -p /export/software/mysql
  wget wget https://cdn.mysql.com/archives/mysql-5.7/mysql-5.7.29-1.el7.x86_64.rpm-bundle.tar
  #上传mysql-5.7.29-1.el7.x86_64.rpm-bundle.tar 到上述文件夹下  解压
  tar xvf mysql-5.7.29-1.el7.x86_64.rpm-bundle.tar
  
  #执行安装
  yum -y install libaio
  
  rpm -ivh mysql-community-common-5.7.29-1.el7.x86_64.rpm mysql-community-libs-5.7.29-1.el7.x86_64.rpm mysql-community-client-5.7.29-1.el7.x86_64.rpm mysql-community-server-5.7.29-1.el7.x86_64.rpm --force --nodeps
  
  warning: mysql-community-common-5.7.29-1.el7.x86_64.rpm: Header V3 DSA/SHA1 Signature, key ID 5072e1f5: NOKEY
  Preparing...                          ################################# [100%]
  Updating / installing...
     1:mysql-community-common-5.7.29-1.e################################# [ 25%]
     2:mysql-community-libs-5.7.29-1.el7################################# [ 50%]
     3:mysql-community-client-5.7.29-1.e################################# [ 75%]
     4:mysql-community-server-5.7.29-1.e################                  ( 49%)
  ```
  
  报错
  
  ```
  警告：mysql-community-common-5.7.29-1.el7.x86_64.rpm: 头V3 DSA/SHA1 Signature, 密钥 ID 5072e1f5: NOKEY
  错误：依赖检测失败：
          mariadb-libs 被 mysql-community-libs-5.7.29-1.el7.x86_64 取代
  ```
  
  解决
  
  ```sh
  #一个命令：解决
  yum remove mysql-libs
  #清除之前安装过的依赖即可
  ```

- mysql初始化设置
  
  ```sh
  #初始化
  mysqld --initialize
  ```
  
  报错
  
  ```txt
  mysqld: error while loading shared libraries: libnuma.so.1: cannot open shared object file: No such file or directory
  ```
  
  解决
  
  ```sh
  yum install -y libaio
  yum -y install numactl
  ```
  
  继续
  
  ```sh
  #初始化
  mysqld --initialize
  
  #更改所属组
  chown mysql:mysql /var/lib/mysql -R
  
  #启动mysql
  systemctl start mysqld.service
  # 关闭
  systemctl stop mysqld.service
  
  #查看生成的临时root密码
  cat  /var/log/mysqld.log
  
  [Note] A temporary password is generated for root@localhost: &=u/1hEVBG!
  ```

- 修改root密码 授权远程访问 设置开机自启动
  
  ```shell
  mysql -u root -p
  Enter password:     #这里输入在日志中生成的临时密码
  Welcome to the MySQL monitor.  Commands end with ; or \g.
  Your MySQL connection id is 3
  Server version: 5.7.29
  
  Copyright (c) 2000, 2020, Oracle and/or its affiliates. All rights reserved.
  
  Oracle is a registered trademark of Oracle Corporation and/or its
  affiliates. Other names may be trademarks of their respective
  owners.
  
  Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.
  
  mysql> 
  ```

  更新root密码  设置为hadoop
  
  ```
  mysql> alter user user() identified by "YuanLai21!";
  Query OK, 0 rows affected (0.00 sec)
  ```

  授权

  ```sql
  mysql> use mysql;
  mysql> GRANT ALL PRIVILEGES ON *.* TO 'root'@'%' IDENTIFIED BY 'YuanLai21!' WITH GRANT OPTION;
  mysql> FLUSH PRIVILEGES; 
  ```
  
  mysql的启动和关闭 状态查看 （这几个命令必须记住）

  ```sh
  systemctl stop mysqld
  systemctl status mysqld
  systemctl start mysqld
  systemctl restart mysqld
  ```
  
  建议设置为开机自启动服务
  
  ```sh
  systemctl enable  mysqld
  ```
  
  Created symlink from /etc/systemd/system/multi-user.target.wants/mysqld.service to /usr/lib/systemd/system/mysqld.service.
  
  查看是否已经设置自启动成功
  
  ```sh
  systemctl list-unit-files | grep mysqld
  ```
  
  mysqld.service                                enabled 

## 卸载

```sh
- Centos7 干净卸载mysql 5.7

```shell
#关闭mysql服务
systemctl stop mysqld.service

#查找安装mysql的rpm包
[root@node3 ~]# rpm -qa | grep -i mysql      
mysql-community-libs-5.7.29-1.el7.x86_64
mysql-community-common-5.7.29-1.el7.x86_64
mysql-community-client-5.7.29-1.el7.x86_64
mysql-community-server-5.7.29-1.el7.x86_64

#卸载
[root@node3 ~]# yum remove mysql-community-libs-5.7.29-1.el7.x86_64 mysql-community-common-5.7.29-1.el7.x86_64 mysql-community-client-5.7.29-1.el7.x86_64 mysql-community-server-5.7.29-1.el7.x86_64

#查看是否卸载干净
rpm -qa | grep -i mysql

#查找mysql相关目录 删除
[root@node1 ~]# find / -name mysql
/var/lib/mysql
/var/lib/mysql/mysql
/usr/share/mysql

[root@node1 ~]# rm -rf /var/lib/mysql
[root@node1 ~]# rm -rf /var/lib/mysql/mysql
[root@node1 ~]# rm -rf /usr/share/mysql

#删除默认配置 日志
rm -rf /etc/my.cnf 
rm -rf /var/log/mysqld.log
```

