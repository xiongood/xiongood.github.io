---
title: docker安装oracle-11
img: https://img.myfox.fun/img/oracle.jpg
categories:
 - 数据库
tags:
 - orcle
 - linux
---

## 出处

```http
https://segmentfault.com/a/1190000020633619?utm_source=tag-newest
```

## 安装oracle

### 安装docker

```sh
[root@localhost ~]# yum install -y docker
```

### 启动docker

```sh
[root@localhost ~]# systemctl start docker
```

### 拉取镜像

```sh
docker pull registry.cn-hangzhou.aliyuncs.com/helowin/oracle_11g
```

镜像大概有6.8G

### 创建容器

```sh
docker images
docker run -d -p 1521:1521 --name oracle_11g registry.aliyuncs.com/helowin/oracle_11g
```

### 启动容器

```sh
docker start oracle_11g
```

### 进入控制台设置用户信息：

```sh
docker exec -it oracle_11g bash
```

### 切换成root进行操作：

```sh
su - root
输入密码   
helowin
```

### 设置oracle环境变量如下：

```sh
vi /etc/profile文件末尾添加：
export ORACLE_HOME=/home/oracle/app/oracle/product/11.2.0/dbhome_2
export ORACLE_SID=helowin
export PATH=${ORACLE_HOME}/bin:$PATH
```

### 切换回oracle用户：

```sh
su - oracle	
```

## 修改sys、system用户密码

```sql
sqlplus /nolog
conn /as sysdba
alter user system identified by oracle; -- 密码为oracle
alter user sys identified by oracle;	-- 密码为oracle
ALTER PROFILE DEFAULT LIMIT PASSWORD_LIFE_TIME UNLIMITED;
```

### 查看sid

```sql
select INSTANCE_NAME from v$instance;
```

一般默认值为：
orcl

### 登录

密码为 oracle

![image-20220118220907310](https://img.myfox.fun/img/image-20220118220907310.png)

## 创建用户		



```sql
-- 创建用户
create user zhangyixiong identified by zhangyixiong;
-- 创建表空间
create tablespace tablespacename datafile '/home/oracle/data/data1' size 1024m;
-- 给用户分配表空间
ALTER user zhangyixiong default tablespace tablespacename;
-- 给用户分配权限
grant create session,create table,unlimited tablespace to zhangyixiong;

grant create session to zhangyixiong;-- //授予zhangsan用户创建session的权限，即登陆权限，允许用户登录数据库

grant unlimited tablespace to zhangyixiong;--  //授予zhangsan用户使用表空间的权限

grant create table to zhangyixiong;-- //授予创建表的权限


grant create session to zhangyixiong;-- //授予zhangsan用户创建session的权限，即登陆权限，允许用户登录数据库

grant unlimited tablespace to zhangyixiong;--  //授予zhangsan用户使用表空间的权限

grant create tablespace  to zhangyixiong;-- //授予创建表的权限

grant drop tablespace  to zhangyixiong;-- //授予删除表的权限
grant unlimited tablespace to zhangyixiong;

grant create tablespace to zhangyixiong;

grant alter tablespace to zhangyixiong;

grant drop tablespace to zhangyixiong;

grant manage tablespace to zhangyixiong;
grant create table to zhangyixiong;
grant create view to zhangyixiong;
grant create trigger to zhangyixiong;
grant create procedure to zhangyixiong;
grant create sequence to zhangyixiong;
```



### 以下为参考

```sql
管理用户

　　create user zhangsan;//在管理员帐户下，创建用户zhangsan

　　alert user scott identified by tiger;//修改密码

授予权限

　　1、默认的普通用户scott默认未解锁，不能进行那个使用，新建的用户也没有任何权限，必须授予权限

　　

　　grant create session to zhangsan;//授予zhangsan用户创建session的权限，即登陆权限，允许用户登录数据库

　　grant unlimited tablespace to zhangsan;//授予zhangsan用户使用表空间的权限

　　grant create table to zhangsan;//授予创建表的权限

　　grante drop table to zhangsan;//授予删除表的权限

　　grant insert table to zhangsan;//插入表的权限

　　grant update table to zhangsan;//修改表的权限

　　grant all to public;//这条比较重要，授予所有权限(all)给所有用户(public)

　　2、oralce对权限管理比较严谨，普通用户之间也是默认不能互相访问的，需要互相授权

　　

　　grant select on tablename to zhangsan;//授予zhangsan用户查看指定表的权限

　　grant drop on tablename to zhangsan;//授予删除表的权限

　　grant insert on tablename to zhangsan;//授予插入的权限

　　grant update on tablename to zhangsan;//授予修改表的权限

　　grant insert(id) on tablename to zhangsan;

　　grant update(id) on tablename to zhangsan;//授予对指定表特定字段的插入和修改权限，注意，只能是insert和update

　　grant alert all table to zhangsan;//授予zhangsan用户alert任意表的权限

　　五、撤销权限

　　基本语法同grant,关键字为revoke

　　六、查看权限

　　select * from user_sys_privs;//查看当前用户所有权限

　　select * from user_tab_privs;//查看所用用户对表的权限
```

