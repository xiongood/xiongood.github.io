---
title: docker的安装与使用
summary: 有了docker，就可以偷懒了，安装电脑软件的时候，再也不用手写各种配置了！
categories:
 - 工具
tags:
 - docker
---

## centos7安装docker

### 更新

```sh
yum -y update
```

### 卸载

```sh
yum remove docker  docker-common docker-selinux docker-engine
```

### 安装

```sh
# 安装必要工具
yum install -y yum-utils device-mapper-persistent-data lvm2
# 更新阿里源
yum-config-manager --add-repo http://mirrors.aliyun.com/docker-ce/linux/centos/docker-ce.repo
# 更新yum索引列表并安装Docker引擎
yum makecache fast
# 安装docker
yum install docker-ce
```

## 启动

### 启动

```sh
service docker start
```

### 查看版本号

```sh
docker version
```

### 常用命令

```sh
# 启动
service docker start
# 停止
service docker stop
```

## 配置镜像仓库

### 官网

```http
https://www.aliyun.com/
```

![image-20230615151944172](https://img.myfox.fun/img/20230615151945.png)

![image-20230615152120708](https://img.myfox.fun/img/20230615152121.png)

### 配置

```sh
sudo mkdir -p /etc/docker
sudo tee /etc/docker/daemon.json <<-'EOF'
{
  "registry-mirrors": ["https://fu5ekmhh.mirror.aliyuncs.com"]
}
EOF
sudo systemctl daemon-reload
sudo systemctl restart docker




sudo mkdir -p /etc/docker
sudo tee /etc/docker/daemon.json <<-'EOF'
{
  "registry-mirrors": ["http://mirrors.ustc.edu.cn/"]
}
EOF
sudo systemctl daemon-reload
sudo systemctl restart docker


```

### 测试

```sh
docker run hello-world
ps -ef | grep docker
docker images
```

### 其他配置

#### 创建新的存储位置

```shell
# 停止docker
service docker stop
# 新建位置
mkdir -p /home/dockerRoot
# 复制源文件
cp -a /var/lib/docker /home/dockerRoot/
# 备份文件
mv -u /var/lib/docker/ /var/lib/docker.bak
# 修改存储位置
vim /etc/docker/daemon.json
```

```json
{
  "registry-mirrors": ["https://你只自己的.mirror.aliyuncs.com"],
  "data-root":"/home/dockerRooot/docker"
}
```

```shell
# 重启docker
service docker start
# 查看
docker info
```

![image-20230615153237805](https://img.myfox.fun/img/20230615153238.png)

## 常用命令

### 下载镜像

```sh
# 查询
docker search nginx
# 下载
docker pull nginx
# 查询本地列表
docker images
```

### 删除镜像

```shell
docker rmi nginx
docker rmi -f nginx
```

### 启动

```shell
# -d 后台运行
docker run -d nginx


#-d 后台运行
#-p 端口映射 （可以有多个 因为该镜像可能存在多个端口）
#rabbitmq:management  (格式 REPOSITORY:TAG)，如果不指定tag，默认使用最新的
#--name  给该容器取个名字
docker run -d --name "xiaoxiao" -p 5672:5672 -p 15672:15672 nginx:latest
```

### 查看

```shell
docker ps
```

### 停止

```shell
docker stop f85489cc894c
```

### 关于容器

```sh
# 停止容器
docker stop 容器名称
# 开启容器
docker start 容器名称
# 移除容器
docker rm 容器名称 （容器必须是停止状态）
```

## springboot上传到自己的仓库

### 修改docker配置

```sh
vim /lib/systemd/system/docker.service
```

```sh
#ExecStart=/usr/bin/dockerd -H fd:// --containerd=/run/containerd/containerd.sock
ExecStart=/usr/bin/dockerd -H tcp://0.0.0.0:2375 -H unix:///var/run/docker.sock
```

### 重启docker

```sh
systemctl daemon-reload
systemctl restart docker
```

### 测试

```http
http://192.168.1.58:2375/version
```

![image-20230615163049661](https://img.myfox.fun/img/20230615163050.png)

### idea配置

![image-20230615163331382](https://img.myfox.fun/img/20230615163332.png)

![image-20230615163511717](https://img.myfox.fun/img/20230615163512.png)



### docker下载jdk8

```shell
docker pull java:8
```


### 创建springboot项目

新建Dockerfile文件

```txt
FROM java:8
EXPOSE 8080
MAINTAINER zhangyixiong
ADD ./demo-docker-1.jar  demo-docker-1.jar
CMD java -jar demo-docker-1.jar
```

```txt
FROM java:8 ## 依赖的包
EXPOSE 8080 ## 使用的端口
MAINTAINER zhangyixiong ## 作者
# 第一个是jar包的位置 第二个是复制到容器里面去的位置
ADD ./demo-docker-1.jar  demo-docker-1.jar ## 复制jar包
CMD java -jar demo-docker-1.jar ## 启动命令
```

### 新增pom插件

注意注意注意注意！！！！！！！！！！！！！！！

<artifactId>demo-common</artifactId> 名字不能有大写

```xml
<build>
        <finalName>${project.artifactId}</finalName>
        <plugins>
            <plugin>
                <groupId>org.apache.maven.plugins</groupId>
                <artifactId>maven-compiler-plugin</artifactId>
                <configuration>
                    <source>1.8</source>
                    <target>1.8</target>
                    <encoding>UTF-8</encoding>
                </configuration>
            </plugin>
            <plugin>
                <groupId>org.springframework.boot</groupId>
                <artifactId>spring-boot-maven-plugin</artifactId>
                <version>2.6.0</version>
                <configuration>
                    <fork>true</fork>
                </configuration>
            </plugin>
            <!-- 跳过单元测试 -->
            <plugin>
                <groupId>org.apache.maven.plugins</groupId>
                <artifactId>maven-surefire-plugin</artifactId>
                <configuration>
                    <skipTests>true</skipTests>
                </configuration>
            </plugin>
            <!--使用docker-maven-plugin插件-->
            <plugin>
                <groupId>com.spotify</groupId>
                <artifactId>docker-maven-plugin</artifactId>
                <version>1.2.0</version>
                <!--将插件绑定在某个phase执行-->
                <executions>
                    <execution>
                        <id>build-image</id>
                        <!--用户只需执行mvn package ，就会自动执行mvn docker:build-->
                        <phase>package</phase>
                        <goals>
                            <goal>build</goal>
                        </goals>
                    </execution>
                </executions>
                <configuration>
                    <!--指定生成的镜像名-->
                    <imageName>docker/${project.artifactId}</imageName>
                    <!--指定标签-->
                    <imageTags>
                        <imageTag>latest</imageTag>
                    </imageTags>
                    <!-- 指定 Dockerfile 路径-->
                    <dockerDirectory>./</dockerDirectory>
                    <!--指定远程 docker api地址-->
                    <dockerHost>http://192.168.1.58:2375</dockerHost>
                    <!-- 这里是复制 jar 包到 docker 容器指定目录配置 -->
                    <resources>
                        <resource>
                            <targetPath>/</targetPath>
                            <!--jar 包所在的路径 此处配置的 即对应 target 目录-->
                            <directory>${project.build.directory}</directory>
                            <!-- 需要包含的 jar包 ，这里对应的是 Dockerfile中添加的文件名 -->
                            <include>${project.build.finalName}.jar</include>
                        </resource>
                    </resources>
                </configuration>
            </plugin>
        </plugins>
    </build>
```

### 完整的pom

```xml
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 https://maven.apache.org/xsd/maven-4.0.0.xsd">

    <parent>
        <groupId>com.xiong</groupId>
        <artifactId>demo</artifactId>
        <version>0.0.1-SNAPSHOT</version>
    </parent>

    <modelVersion>4.0.0</modelVersion>
    <groupId>com.xiong</groupId>
    <artifactId>demo-docker-1</artifactId>
    <version>0.0.1-SNAPSHOT</version>
    <name>demo-docker-1</name>
    <description>demo-docker-1</description>
    <properties>
        <java.version>1.8</java.version>
        <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
        <project.reporting.outputEncoding>UTF-8</project.reporting.outputEncoding>
        <spring-boot.version>2.7.5</spring-boot.version>
    </properties>

    <dependencies>
        <dependency>
            <groupId>com.xiong</groupId>
            <artifactId>demo-common</artifactId>
            <version>0.0.1-SNAPSHOT</version>
        </dependency>
    </dependencies>

    <build>
        <finalName>${project.artifactId}</finalName>
        <plugins>
            <plugin>
                <groupId>org.apache.maven.plugins</groupId>
                <artifactId>maven-compiler-plugin</artifactId>
                <configuration>
                    <source>1.8</source>
                    <target>1.8</target>
                    <encoding>UTF-8</encoding>
                </configuration>
            </plugin>
            <plugin>
                <groupId>org.springframework.boot</groupId>
                <artifactId>spring-boot-maven-plugin</artifactId>
                <version>2.6.0</version>
                <configuration>
                    <fork>true</fork>
                </configuration>
            </plugin>
            <!-- 跳过单元测试 -->
            <plugin>
                <groupId>org.apache.maven.plugins</groupId>
                <artifactId>maven-surefire-plugin</artifactId>
                <configuration>
                    <skipTests>true</skipTests>
                </configuration>
            </plugin>
            <!--使用docker-maven-plugin插件-->
            <plugin>
                <groupId>com.spotify</groupId>
                <artifactId>docker-maven-plugin</artifactId>
                <version>1.2.0</version>
                <!--将插件绑定在某个phase执行-->
                <executions>
                    <execution>
                        <id>build-image</id>
                        <!--用户只需执行mvn package ，就会自动执行mvn docker:build-->
                        <phase>package</phase>
                        <goals>
                            <goal>build</goal>
                        </goals>
                    </execution>
                </executions>
                <configuration>
                    <!--指定生成的镜像名-->
                    <imageName>docker/${project.artifactId}</imageName>
                    <!--指定标签-->
                    <imageTags>
                        <imageTag>latest</imageTag>
                    </imageTags>
                    <!-- 指定 Dockerfile 路径-->
                    <dockerDirectory>./</dockerDirectory>
                    <!--指定远程 docker api地址-->
                    <dockerHost>http://192.168.1.58:2375</dockerHost>
                    <!-- 这里是复制 jar 包到 docker 容器指定目录配置 -->
                    <resources>
                        <resource>
                            <targetPath>/</targetPath>
                            <!--jar 包所在的路径 此处配置的 即对应 target 目录-->
                            <directory>${project.build.directory}</directory>
                            <!-- 需要包含的 jar包 ，这里对应的是 Dockerfile中添加的文件名 -->
                            <include>${project.build.finalName}.jar</include>
                        </resource>
                    </resources>
                </configuration>
            </plugin>
        </plugins>
    </build>
</project>

```

### 构建

先打包，然后再构建，构建时，dockerfile要和jar包放到同一个文件夹下



![image-20230615170606973](https://img.myfox.fun/img/20230615170608.png)

### 查看

已经有了该镜像

![image-20230615165154420](https://img.myfox.fun/img/20230615165155.png)



### 启动容器

![image-20230615170705036](https://img.myfox.fun/img/20230615170706.png)

![image-20230615172021720](https://img.myfox.fun/img/20230615172022.png)

![image-20230615172107289](https://img.myfox.fun/img/20230615172108.png)

### 查看

![image-20230615172139135](https://img.myfox.fun/img/20230615172140.png)

## 安装Portainer

### 安装

```sh
docker volume create portainer_data
docker run -d -p 9000:9000 -v /var/run/docker.sock:/var/run/docker.sock -v portainer_data:/data portainer/portainer
```

参数说明

```txt
-d	#容器在后台运行
-p 9000:9000	#宿主机9000端口映射容器中的9000端口，容器的默认端口为9000
-v /var/run/docker.sock:/var/run/docker.sock	#重点配置参数，把宿主机的Docker守护进程(docker daemon)默认监听的Unix域套接字挂载到容器中
-v /root/portainer:/data	#把宿主机目录 /root/portainer 挂载到容器 /data 目录；
-name portainer	#指定运行容器的名称，这里会自动去容器的镜像站下载该镜像
```

### 查看是否启动

```sh
docker images
docker ps -a
```

### 访问

```http
http://192.168.159.128:9000/#!/init/admin
```

### 创建用户

密码必须大于12位

Xiong1991!@#

![image-20240830092158877](https://img.myfox.fun/img/image-20240830092158877.png)

### 查看运行情况

![image-20240830092403839](https://img.myfox.fun/img/image-20240830092403839.png)

![image-20240830092607601](https://img.myfox.fun/img/image-20240830092607601.png)

### 查看日志

![image-20240830092645322](https://img.myfox.fun/img/image-20240830092645322.png)

![image-20240830092712090](https://img.myfox.fun/img/image-20240830092712090.png)

## 开机启动docker

```sh
开机启动
docker update --restart=always 容器ID
 
取消
docker update --restart=no 容器ID 
```

