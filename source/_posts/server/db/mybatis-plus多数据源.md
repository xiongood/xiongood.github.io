---
title: mybatis-plus多数据源
img: https://gitee.com/xiongood/image/raw/master/mybatis.jpg
categories:
 - 后端
tags:
 - mybatis-plus
 - java
---

## 单数据源实现

### 准备

- 创建表

```sql
SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

DROP TABLE IF EXISTS `t_user`;
CREATE TABLE `t_user`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `uname` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `pwd` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1650429143901097987 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

SET FOREIGN_KEY_CHECKS = 1;
```

### pom

```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-web</artifactId>
</dependency>

<dependency>
    <groupId>org.projectlombok</groupId>
    <artifactId>lombok</artifactId>
    <optional>true</optional>
</dependency>
<dependency>
    <groupId>cn.hutool</groupId>
    <artifactId>hutool-all</artifactId>
    <version>5.8.16</version>
</dependency>

<dependency>
    <groupId>org.mybatis.spring.boot</groupId>
    <artifactId>mybatis-spring-boot-starter</artifactId>
    <version>3.0.0</version>
</dependency>
<dependency>
    <groupId>com.baomidou</groupId>
    <artifactId>mybatis-plus-boot-starter</artifactId>
    <version>3.4.0</version>
</dependency>
<dependency>
    <groupId>mysql</groupId>
    <artifactId>mysql-connector-java</artifactId>
    <version>8.0.19</version>
</dependency>
```

### application.yml

```yaml
server:
  port: 8080
spring:
  profiles:
    active: 单表

mybatis-plus:
  mapper-locations: mapper/*.xml
  configuration:
    log-impl: org.apache.ibatis.logging.stdout.StdOutImpl
  type-aliases-package: com.xiong.demo.entity
logging:
  config: classpath:logback.xml
```

### application-单表.yml

```yaml
spring:
  datasource:
    url: jdbc:mysql://192.168.43.89:3306/db_user?serverTimezone=UTC&useUnicode=true&characterEncoding=utf-8&AllowPublicKeyRetrieval=True
    username: root
    password: 123456
```

### 实体类

```java
import com.baomidou.mybatisplus.annotation.IdType;
import com.baomidou.mybatisplus.annotation.TableField;
import com.baomidou.mybatisplus.annotation.TableId;
import com.baomidou.mybatisplus.annotation.TableName;
import lombok.Data;

@Data
@TableName(value = "t_user")
public class TUser {
    @TableId(value = "id", type = IdType.ASSIGN_ID)
    private Long id;

    @TableField(value = "uname")
    private String uname;

    @TableField(value = "pwd")
    private String pwd;
}
```

### mapper

```java
import com.baomidou.mybatisplus.core.mapper.BaseMapper;
import com.xiong.demo.entity.TDict;
import org.apache.ibatis.annotations.Mapper;

@Mapper
public interface TDictMapper extends BaseMapper<TDict> {
}
```

### service

```java
import org.springframework.stereotype.Service;
import javax.annotation.Resource;
import java.util.List;
import com.baomidou.mybatisplus.extension.service.impl.ServiceImpl;
import com.xiong.demo.mapper.TUserMapper;
import com.xiong.demo.entity.TUser;
import com.xiong.demo.service.TUserService;
@Service
public class TUserServiceImpl extends ServiceImpl<TUserMapper, TUser> implements TUserService{

}
```

### impl

```java
import org.springframework.stereotype.Service;
import com.baomidou.mybatisplus.extension.service.impl.ServiceImpl;
import com.xiong.demo.entity.TDict;
import com.xiong.demo.mapper.TDictMapper;
import com.xiong.demo.service.TDictService;
@Service
public class TDictServiceImpl extends ServiceImpl<TDictMapper, TDict> implements TDictService{

}

```

### controller

```java
import com.xiong.demo.entity.TUser;
import com.xiong.demo.service.TUserService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/single")
public class SingleController {

    @Autowired
    TUserService tUserService;

    // 测试新增
    @GetMapping("/testInster")
    public void testInster(){
        TUser tUser = new TUser();
        tUser.setPwd("aaa");
        tUser.setUname("测试单表");
        tUserService.save(tUser);
    }

}
```

### 测试

```http
http://localhost:8080/single/testInster
```

## 多数据源实现

### 方式一 主从复制（一主多从）

### 准备

略

### pom

```xml
<dependency>
    <groupId>com.baomidou</groupId>
    <artifactId>dynamic-datasource-spring-boot-starter</artifactId>
    <version>3.6.1</version>
</dependency>
```

