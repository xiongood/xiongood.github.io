---
title: centos7安装oms
---



## 系统准备

centos7

核心数：大于等于8

内存：12G

硬盘：500G

提前准备一个ob数据库，用来作为RM CM 库。

## 安装

### 启动docker

```sh
service docker start
```

### 常用命令

```sh
# 进入容器
docker exec -it eb79568a3807  /bin/bash

```



### 创建文件目录

```sh
mkdir -p /opt/oms
# 把oms_4.2.11-ce.tar.gz放到该目录下
```

### 创建挂在目录

```sh
mkdir -p /opt/omsData
cd  /opt/omsData
mkdir -p ./home/admin/logs
mkdir -p ./home/ds/store
mkdir -p ./home/ds/run
```

### 加载docker

```sh
# 示例
docker load -i <OMS 安装包>
# 命令
docker load -i oms_4.2.11-ce.tar.gz

# 查看
docker images
```

### 从加载的镜像中获取部署脚本 `docker_remote_deploy.sh`

```sh
# 示例
sudo docker run -d --net host --name oms-config-tool <OMS_IMAGE> bash && sudo docker cp oms-config-tool:/root/docker_remote_deploy.sh . && sudo docker rm -f oms-config-tool
# 命令
sudo docker run -d --net host --name oms-config-tool reg.docker.alibaba-inc.com/oceanbase/oms-ce:feature_4.2.11_ce bash && sudo docker cp oms-config-tool:/root/docker_remote_deploy.sh . && sudo docker rm -f oms-config-tool

```

### 启动

注意：启动成功后多等一会儿才行

```sh
# 示例
sh docker_remote_deploy.sh -o <OMS 容器挂载目录> -i <本机 IP 地址> -d <OMS_IMAGE>

# 命令
sh docker_remote_deploy.sh -o /opt/omsData -i  192.168.1.60  -d reg.docker.alibaba-inc.com/oceanbase/oms-ce:feature_4.2.11_ce 
```

## 使用

### 访问

```http
http://192.168.1.60:8089/
```

### 设置密码

初次登录 设置admin 和root的密码

```txt
XIong1991!@#
```



