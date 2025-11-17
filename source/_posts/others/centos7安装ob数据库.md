---
title: centos7安装ob数据库
---

## 下载

略

## 安装

### 安装

```sh
tar -xzf oceanbase-all-in-one-*.tar.gz
cd oceanbase-all-in-one/bin/
./install.sh
cd ../../
source ~/.oceanbase-all-in-one/bin/env.sh
```

### 启动

**注意看账号的密码**

```sh
obd demo # 启动
obd cluster restart demo # 重启
```

#### 可能的错误

```txt
[ERROR] OBD-1007:(127.0.0.1) open files must not be less than 20000 (Current value: 1024)……………………
```

#### 解决方案一

先保证内存在3G以上

然后可以尝试执行如下配置

```sh
vim /etc/security/limits.conf 
```

在最后新增

```txt
* soft nofile 655360
* hard nofile 655360
* soft nproc 655360
* hard nproc 655360
* soft core unlimited
* hard core unlimited
* soft stack unlimited
* hard stack unlimited
```

### 查看状态

```sh
obd cluster list
```

## 使用

### 连接数据库

```sh
# 密码在日志中
obclient -h127.0.0.1 -P2881 -uroot@sys -Doceanbase -A -p
# 密码：
# root VoeOD0iW3MZyMgTLy31r
# admim K6uuRZaJuX


# 设置远程访问
GRANT ALL PRIVILEGES ON oceanbase.* TO 'root'@'%';
```

![image-20251107113716534](http://img.myfox.fun/img/image-20251107113716534.png)

### 设置远程连接

```sh
# 创建用户
CREATE USER 'demo'@'%' IDENTIFIED BY '12345678';
# 设置密码
GRANT ALL PRIVILEGES ON oceanbase.* TO 'demo'@'%';
```

### 工具链接

使用和mysql配置一致即可

![image-20251107114556270](http://img.myfox.fun/img/image-20251107114556270.png)

![image-20251107115000609](http://img.myfox.fun/img/image-20251107115000609.png)