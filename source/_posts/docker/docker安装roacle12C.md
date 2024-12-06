---
title: docker安装oracle12C
summary: 感觉如果手动安装oracle实在是太费劲了，所以偷懒用了dockers，学习测试使用
img: https://img.myfox.fun/img/oracle.jpg
categories:
 - 数据库
tags:
 - orcle
 - linux
---



## 安装docker

```shell
yum install docker
service docker start
docker version
```

## 安装oracle

```shell
# 拉去镜像
docker pull truevoly/oracle-12c

# 挂载目录
mkdir -p /data/oracle/data_temp  && chmod 777 /data/oracle/data_temp

# 启动容器
docker run --restart always -d -p 8080:8080 -p 1521:1521 -v /data/oracle/data_temp:/home/oracle/data_temp   -v /etc/localtime:/etc/localtime:ro  --name orcl truevoly/oracle-12c  --privileged=true

# 查看容器
docker ps
# 查看oracle的日志
docker logs -f 106ba99a5ac8
```

## 设置oracle

```sh
docker exec -it orcl /bin/bash
# 切换成oracle用户
su oracle
# 进入sqlplus
$ORACLE_HOME/bin/sqlplus / as sysdba
# 设置密码有效期为无限制
SQL> ALTER PROFILE DEFAULT LIMIT PASSWORD_LIFE_TIME UNLIMITED;
# 解锁system用户
SQL> alter user SYSTEM account unlock;
# 给system设置sysdba权限（密码是 oracle）
SQL> conn  sys as sysdba
SQL> grant sysdba to system;
```

## 连接

### idea

![image-20230829142129995](https://img.myfox.fun/img/20230829142131.png)

```shell
账户：system
密码：oracle
```

### plsql

在tnsnames.ora中新增如下

```txt
xe =
  (DESCRIPTION =
    (ADDRESS = (PROTOCOL = TCP)(HOST = 192.168.43.96)(PORT = 1521))
    (CONNECT_DATA =
      (SERVER = DEDICATED)
      (SERVICE_NAME = xe)
    )
  )
```

![image-20230829143848859](https://img.myfox.fun/img/20230829143850.png)

登录

![image-20230829143943869](https://img.myfox.fun/img/20230829143944.png)
