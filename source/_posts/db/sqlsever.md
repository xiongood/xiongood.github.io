---
title: sqlsever的安装
img: https://gitee.com/xiongood/image/raw/master/sqlserver.jpg
categories:
 - 数据库
tags:
 - sqlsever
 - linux
---

## 安装sqlsever

- 官网

```http
https://docs.microsoft.com/zh-cn/sql/linux/sql-server-linux-setup?view=sql-server-ver15
```

```http
https://docs.microsoft.com/zh-cn/sql/linux/quickstart-install-connect-red-hat?view=sql-server-ver15
```

- 准备

```sh
sudo alternatives --config python
# If not configured, install python2 and openssl10 using the following commands: 
sudo yum install python2
sudo yum install compat-openssl10
# Configure python2 as the default interpreter using this command: 
sudo alternatives --config python
```

- 安装

```sh
# 下载 Microsoft SQL Server 2019 Red Hat 存储库配置文件：
sudo curl -o /etc/yum.repos.d/mssql-server.repo https://packages.microsoft.com/config/rhel/7/mssql-server-2019.repo

# 运行以下命令以安装 SQL Server：
sudo yum install -y mssql-server

# 包安装完成后，运行 mssql-conf setup，按照提示设置 SA 密码并选择版本。
# 请确保为 SA 帐户指定强密码（最少 8 个字符，包括大写和小写字母、十进制数字和/或非字母数字符号）。
sudo /opt/mssql/bin/mssql-conf setup
# 密钥 PMBDC-FXVM3-T777P-N4FY8-PKFF4
# Xiong1991.X

# 完成配置后，验证服务是否正在运行：
systemctl status mssql-server

#若要允许远程连接，请在 RHEL 的防火墙上打开 SQL Server 端口。 默认的 SQL Server 端口为 TCP 1433。 如果为防火墙使用的是 FirewallD，则可以使用以下命令：
sudo firewall-cmd --zone=public --add-port=1433/tcp --permanent
sudo firewall-cmd --reload
```

--  至此安装完毕

## 连接sqlsever

![image-20220329182556726](https://gitee.com/xiongood/image/raw/master/image-20220329182556726.png)

- 安装命令行链接

```sh
# 下载
sudo curl -o /etc/yum.repos.d/msprod.repo https://packages.microsoft.com/config/rhel/7/prod.repo
sudo yum install -y mssql-tools unixODBC-devel

#为方便起见，请 /opt/mssql-tools/bin/ 添加到 /opt/mssql-tools/bin/ 环境变量。 这样可以在不指定完整路径的情况下运行这些工具。 运行以下命令以修改登录会话和交互式/非登录会话的路径 ：

echo 'export PATH="$PATH:/opt/mssql-tools/bin"' >> ~/.bash_profile
echo 'export PATH="$PATH:/opt/mssql-tools/bin"' >> ~/.bashrc
source ~/.bashrc

```

- 本地链接

```sh
sqlcmd -S localhost -U SA -P '<YourPassword>'

# 可以在命令行上省略密码，以收到密码输入提示。
# 如果以后决定进行远程连接，请指定 -S 参数的计算机名称或 IP 地址，并确保防火墙上的端口 1433 已打开。
```

- 创建数据库

```sql
-- 创建
CREATE DATABASE TestDB
-- SELECT Name from sys.Databases

-- 前两个命令没有立即执行。 必须在新行中键入 GO 才能执行以前的命令：
GO

-- 新增
USE TestDB
CREATE TABLE Inventory (id INT, name NVARCHAR(50), quantity INT)
INSERT INTO Inventory VALUES (1, 'banana', 150); INSERT INTO Inventory VALUES (2, 'orange', 154);
GO

-- 查询
SELECT * FROM Inventory WHERE quantity > 152;
GO
```

## springboot 整合 sqlsever

- 项目结构

```TXT
├─src
│  ├─main
│  │  ├─java
│  │  │  └─com
│  │  │      └─example
│  │  │          └─sqlsever1
│  │  │              ├─controller
│  │  │              └─mapper
│  │  └─resources
│  │      ├─mapper
│  │      └─mybatis
```

- pom

```xml
<dependency>
    <groupId>com.microsoft.sqlserver</groupId>
    <artifactId>sqljdbc4</artifactId>
    <version>4.0</version>
</dependency>
<dependency>
    <groupId>org.mybatis.spring.boot</groupId>
    <artifactId>mybatis-spring-boot-starter</artifactId>
    <version>1.3.2</version>
</dependency>
```

- yml

```yml
spring:
  datasource:
    driver-class-name: com.microsoft.sqlserver.jdbc.SQLServerDriver
    url: jdbc:sqlserver://192.168.1.101:1433;DatabaseName=TestDB
    username: SA
    password: Xiong1991.X
    maxActive: 20
    initialSize: 1
    maxWait: 60000
    minIdle: 1
    timeBetweenEvictionRunsMillis: 60000
    minEvictableIdleTimeMillis: 300000
    validationQuery: select 1
    testWhileIdle: true
    testOnBorrow: true
    testOnReturn: true
    poolPreparedStatements: true
    maxOpenPreparedStatements: 20
mybatis:
  mapper-locations: classpath:mapper/**/*Mapper.xml
```

- xml

```xml
<?xml version="1.0" encoding="UTF-8" ?>
<!DOCTYPE mapper PUBLIC "-//mybatis.org//DTD Mapper 3.0//EN" "http://mybatis.org/dtd/mybatis-3-mapper.dtd" >

<mapper namespace="com.example.sqlsever1.mapper.TestMapper">

    <select id="findAll" resultType="java.lang.Integer">
        select  count (*) from Inventory
    </select>

</mapper>
```

- Mapper.java

```java
package com.example.sqlsever1.mapper;

import org.apache.ibatis.annotations.Mapper;

@Mapper
public interface TestMapper {

    Integer findAll();
}

```

- Controller.java

```java
import com.example.sqlsever1.mapper.TestMapper;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;


@RestController
@RequestMapping("/test")
public class TestController {

    @Autowired
    TestMapper testMapper;

    @GetMapping("/findAll")
    public Integer findAll(){
        return  testMapper.findAll();
    }

}
```

- 启动访问

```http
http://localhost:8080/test/findAll
```









