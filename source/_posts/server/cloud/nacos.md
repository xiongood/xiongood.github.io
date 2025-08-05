---
title: nacos单机版使用
categories:
 - 后端
tags:
 - 微服务
 - nacos
 - java
---

## 说明

### 版本

| 组件               | 版本       |
| ------------------ | ---------- |
| springboot         | 2.6.13     |
| springcloudalibaba | 2021.0.5.0 |
| nacos              | 2.2.0      |

## 官方文档

### 快速开始

```http
https://nacos.io/zh-cn/docs/quick-start.html
```

### 版本说明

```http
https://github.com/alibaba/spring-cloud-alibaba/wiki/%E7%89%88%E6%9C%AC%E8%AF%B4%E6%98%8E
```

## 下载

```http
https://github.com/alibaba/nacos
```

## 启动

### 修改配置文件

认证信息可以忽略

```properties
# 要修改这几个配置
nacos.core.auth.enabled=true
nacos.core.auth.caching.enabled=true
nacos.core.auth.server.identity.key=test
nacos.core.auth.server.identity.value=test
nacos.core.auth.plugin.nacos.token.secret.key=VGhpc0lzTXlDdXN0b21TZWNyZXRLZXkwMTIzNDU2Nzg=
```

### 启动

```sh
startup.cmd -m standalone
```

## 访问

```http
http://localhost:8848/nacos/
```

## 使用数据库

### 配置文件新增

```properties
spring.datasource.platform=mysql
db.num=1
db.url.0=jdbc:mysql://localhost:3306/nacos_devtest?characterEncoding=utf8&connectTimeout=1000&socketTimeout=3000&autoReconnect=true
db.user=root
db.password=123456
```

### 在数据库中运行sql

```txt
mysql-schema.sql
```

## java链接nacos

### 完整的pom

```xml
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 https://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>
    <groupId>com.xiong</groupId>
    <artifactId>demoCloud</artifactId>
    <version>0.0.1-SNAPSHOT</version>
    <name>demoCloud</name>
    <description>demoCloud</description>
    <properties>
        <java.version>1.8</java.version>
        <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
        <project.reporting.outputEncoding>UTF-8</project.reporting.outputEncoding>
        <spring-boot.version>2.6.13</spring-boot.version>
        <spring-cloud-alibaba.version>2021.0.5.0</spring-cloud-alibaba.version>
    </properties>
    <dependencies>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-web</artifactId>
        </dependency>
        <dependency>
            <groupId>com.alibaba.cloud</groupId>
            <artifactId>spring-cloud-starter-alibaba-nacos-discovery</artifactId>
        </dependency>
        <dependency>
            <groupId>com.alibaba.cloud</groupId>
            <artifactId>spring-cloud-starter-alibaba-nacos-config</artifactId>
        </dependency>
        <dependency>
            <groupId>org.springframework.cloud</groupId>
            <artifactId>spring-cloud-starter-bootstrap</artifactId>
            <version>4.0.0</version>
        </dependency>
    </dependencies>
    <dependencyManagement>
        <dependencies>
            <dependency>
                <groupId>org.springframework.boot</groupId>
                <artifactId>spring-boot-dependencies</artifactId>
                <version>${spring-boot.version}</version>
                <type>pom</type>
                <scope>import</scope>
            </dependency>
            <dependency>
                <groupId>com.alibaba.cloud</groupId>
                <artifactId>spring-cloud-alibaba-dependencies</artifactId>
                <version>${spring-cloud-alibaba.version}</version>
                <type>pom</type>
                <scope>import</scope>
            </dependency>
        </dependencies>
    </dependencyManagement>

    <build>
        <plugins>
            <plugin>
                <groupId>org.apache.maven.plugins</groupId>
                <artifactId>maven-compiler-plugin</artifactId>
                <version>3.8.1</version>
                <configuration>
                    <source>1.8</source>
                    <target>1.8</target>
                    <encoding>UTF-8</encoding>
                </configuration>
            </plugin>
            <plugin>
                <groupId>org.springframework.boot</groupId>
                <artifactId>spring-boot-maven-plugin</artifactId>
                <version>${spring-boot.version}</version>
                <configuration>
                    <mainClass>com.xiong.demoCloud.DemoCloudApplication</mainClass>
                    <skip>true</skip>
                </configuration>
                <executions>
                    <execution>
                        <id>repackage</id>
                        <goals>
                            <goal>repackage</goal>
                        </goals>
                    </execution>
                </executions>
            </plugin>
        </plugins>
    </build>

</project>

```

### 配置文件 

application.yml，nacos2.0屏蔽了bootstrap.yml

```yaml
server:
  port: 8080
spring:
  application:
    name: nacos-service
  cloud:
    nacos:
      discovery:
        namespace: public
        password: nacos
        server-addr: localhost:8848
        username: nacos
```

## 启动并查看nacos

![image-20230524171017984](https://img.myfox.fun/img/20230524171020.png)

## nacos做配置中心

### 首先在nacos中新增配置文件

![image-20230526104205837](https://img.myfox.fun/img/20230526104207.png)

### 修改pom

新增config

```xml
<dependency>
    <groupId>com.alibaba.cloud</groupId>
    <artifactId>spring-cloud-starter-alibaba-nacos-config</artifactId>
</dependency>
```

### 修稿配置文件

application.yml

```yaml
server:
  port: 8080
spring:
  application:
    name: nacos-service
  profiles:
    active: dev
  cloud:
    nacos:
      discovery:
        server-addr: localhost:8848
        namespace: public
        username: nacos
        password: nacos
      config:
        group: DEFAULT_GROUP
        server-addr: localhost:8848
        username: nacos
        password: nacos
  config:
    import:
      - optional:nacos:nacos-service-dev.yaml  # 监听 DEFAULT_GROUP:test.yml
      #- optional:nacos:test01.yml?group=group_01 # 覆盖默认 group，监听 group_01:test01.yml
      #- optional:nacos:test02.yml?group=group_02&refreshEnabled=false # 不开启动态刷新
      #- nacos:test03.yml # 在拉取nacos配置异常时会快速失败，会导致 spring 容器启动失败
```

![image-20230526104335176](https://img.myfox.fun/img/20230526104336.png)

### 写测试方法

```java
import org.springframework.beans.factory.annotation.Value;
import org.springframework.cloud.context.config.annotation.RefreshScope;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

/**
 * @Auther: 张一雄
 * @Date: 2023/5/24 17:15
 * @Description: TestController
 * @Version 1.0.0
 */

@RestController
@RequestMapping("/test")
// 自动刷新配置
@RefreshScope
public class TestController {

    @Value("${conf.get}")
    private String test;

    //@NacosValue(value = "${conf.get2}",autoRefreshed=true)
    //private String test2;

    @GetMapping("getAbc")
    public String getAbc(){
        return test;
    }


}

```

### 启动测试

```http
GET http://localhost:8080/test/getAbc
```

可以获得配置中心的配置信息
