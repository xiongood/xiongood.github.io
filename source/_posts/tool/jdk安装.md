---
title: jdk的安装
author: 张一雄
summary: 我们java程序员所依赖的开发运行工具！
tags:
  - jdk
categories:
  - 工具
---

## centos7安装jdk8

### 准备工作

```shell
#1.检查当前机器是否有自带的JDK
rpm -qa |grep java
rpm -qa |grep jdk
rpm -qa |grep gcj
#2.如果没有 则跳至安装步骤，有的话 进行卸载
rpm -qa | grep java | xargs rpm -e --nodeps
#3.检测卸载是否成功
java -version
#出现一下提示则说明没有安装JDK或者已经卸载成功
-bash: java: command not found
```

### 安装

#### 下载解压

下载地址

```http
https://repo.huaweicloud.com/java/jdk/8u151-b12/
```

执行命令

```sh
# 新建目录
cd /opt 
mkdir jdk
cd jdk
# 下载
wget https://repo.huaweicloud.com/java/jdk/8u151-b12/jdk-8u151-linux-x64.tar.gz
# 解压
tar  -zxvf jdk-8u151-linux-x64.tar.gz
# 删除无用包
rm -rf ./jdk-8u151-linux-x64.tar.gz 
```

#### 修改配置文件

```shell
#编辑配置文件
vim /etc/profile
#添加JDK配置
# jdk配置
export JAVA_HOME=/opt/jdk/jdk1.8.0_151
export JRE_HOME=$JAVA_HOME/jre
export PATH=$JAVA_HOME/bin:$JRE_HOME/bin:$PATH
export CLASSPATH=$CLASSPATH:.:$JAVA_HOME/lib:$JRE_HOME/lib
#按esc退出按wq!保存退出

#刷新配置
source /etc/profile
```

### 查看是否成功

```shell
java -version
```

## centost-yum

```sh
# 查看列表
yum list java-1.8.0-openjdk*
# 安装
yum install -y java-1.8.0-openjdk-devel.x86_64
```



### windows

带整理

## centos7安装jdk6

```sh
mkdir -R /opt/jdk
wget https://repo.huaweicloud.com/java/jdk/6u45-b06/jdk-6u45-linux-x64.bin
# 执行安装
./jdk-6u45-linux-x64.bin
# 修改系统变量
vi /etc/profile
```

```txt
export JAVA_HOME=/opt/jdk/jdk1.6.0_45
export JAVA_BIN=/opt/jdk/jdk1.6.0_45/bin
export PATH=$PATH:$JAVA_HOME/bin 
export CLASSPATH=.:$JAVA_HOME/lib/dt.jar:$JAVA_HOME/lib/tools.jar
export JAVA_HOME JAVA_BIN PATH CLASSPATH
```

```sh
#刷新
cd /
. /etc/profile
```

